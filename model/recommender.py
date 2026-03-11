import pandas as pd
import numpy as np
import os
import joblib
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# NLTK Setup
# ---------------------------
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

print("Loading datasets...")

# ---------------------------
# Load Western dataset
# ---------------------------
df1 = pd.read_csv("../data/clean_recipes.csv")

df1 = df1[[
    "Name",
    "ingredients_cleaned",
    "Calories",
    "ProteinContent",
    "RecipeCategory"
]]

df1["Cuisine"] = "Global"

# ---------------------------
# Load Indian dataset
# ---------------------------
ind_df = pd.read_csv("../data/indian_food.csv")

ind_df = ind_df.rename(columns={
    "name": "Name",
    "ingredients": "ingredients_cleaned",
    "course": "RecipeCategory"
})

ind_df["Calories"] = np.nan
ind_df["ProteinContent"] = np.nan
ind_df["Cuisine"] = "Indian"

ind_df = ind_df[[
    "Name",
    "ingredients_cleaned",
    "Calories",
    "ProteinContent",
    "RecipeCategory",
    "Cuisine"
]]

# Align western columns
df1 = df1[[
    "Name",
    "ingredients_cleaned",
    "Calories",
    "ProteinContent",
    "RecipeCategory",
    "Cuisine"
]]

# ---------------------------
# Merge datasets
# ---------------------------
df = pd.concat([df1, ind_df], ignore_index=True)
df = df.dropna(subset=["ingredients_cleaned"])
df["ingredients_cleaned"] = df["ingredients_cleaned"].astype(str)
df = df.reset_index(drop=True)

print("Total combined recipes:", df.shape[0])

# ---------------------------
# Text Normalization
# ---------------------------
SYNONYM_MAP = {
    "paneer": "cottage cheese",
    "capsicum": "bell pepper",
    "chilli": "chili",
    "curd": "yogurt",
    "maida": "flour",
    "atta": "wheat flour",
    "dhaniya": "coriander",
    "jeera": "cumin"
}

def normalize_text(text):
    text = str(text)
    text = text.replace("[", "").replace("]", "").replace("'", "")
    text = text.replace(",", " ")
    words = text.lower().split()

    processed = []
    for w in words:
        w = lemmatizer.lemmatize(w)
        processed.append(SYNONYM_MAP.get(w, w))

    return " ".join(processed)

df["ingredients_cleaned"] = df["ingredients_cleaned"].apply(normalize_text)

# ---------------------------
# TF-IDF Caching
# ---------------------------
CACHE_DIR = "cache"
VECTORIZER_PATH = os.path.join(CACHE_DIR, "tfidf_vectorizer.pkl")
MATRIX_PATH = os.path.join(CACHE_DIR, "tfidf_matrix.pkl")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

if os.path.exists(VECTORIZER_PATH) and os.path.exists(MATRIX_PATH):
    print("Loading cached TF-IDF model...")
    tfidf = joblib.load(VECTORIZER_PATH)
    tfidf_matrix = joblib.load(MATRIX_PATH)
else:
    print("Building TF-IDF matrix...")
    tfidf = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.85
    )
    tfidf_matrix = tfidf.fit_transform(df["ingredients_cleaned"])
    joblib.dump(tfidf, VECTORIZER_PATH)
    joblib.dump(tfidf_matrix, MATRIX_PATH)

print("TF-IDF matrix shape:", tfidf_matrix.shape)

# ---------------------------
# Detect Indian-style query
# ---------------------------
INDIAN_KEYWORDS = {
    "ghee", "paneer", "jeera", "dhaniya",
    "cardamom", "saffron", "masala", "besan"
}

def detect_indian_style(user_ingredients):
    return len(user_ingredients & INDIAN_KEYWORDS) > 0

# ---------------------------
# Recommendation Function
# ---------------------------
def recommend_by_ingredients(
    user_input,
    match_mode="any",
    max_calories=None,
    high_protein=False,
    top_n=5
):

    user_input = normalize_text(user_input)
    user_ingredients = set(user_input.split())

    filtered_df = df.copy()

    # Ingredient filtering
    if match_mode == "all":
        filtered_df = filtered_df[
            filtered_df["ingredients_cleaned"].apply(
                lambda x: user_ingredients.issubset(set(x.split()))
            )
        ]
    else:
        filtered_df = filtered_df[
            filtered_df["ingredients_cleaned"].apply(
                lambda x: len(user_ingredients & set(x.split())) > 0
            )
        ]

    # Calorie filter (allow NaN)
    if max_calories:
        filtered_df = filtered_df[
            (filtered_df["Calories"].isna()) |
            (filtered_df["Calories"] <= max_calories)
        ]

    # High protein filter
    if high_protein:
        filtered_df = filtered_df[
            filtered_df["ProteinContent"].fillna(0) >= 15
        ]

    if filtered_df.empty:
        print("❌ No recipes found.")
        return

    indices = filtered_df.index.tolist()

    user_vector = tfidf.transform([user_input])
    similarity_scores = cosine_similarity(
        user_vector, tfidf_matrix[indices]
    ).flatten()

    is_indian_query = detect_indian_style(user_ingredients)

    final_scores = []

    for i, idx in enumerate(indices):

        recipe_ingredients = set(df.loc[idx, "ingredients_cleaned"].split())
        overlap = len(user_ingredients & recipe_ingredients)

        cuisine_boost = 0
        if is_indian_query and df.loc[idx, "Cuisine"] == "Indian":
            cuisine_boost = 0.15

        final_score = (
            0.7 * similarity_scores[i] +
            0.25 * (overlap / max(1, len(user_ingredients))) +
            cuisine_boost
        )

        final_scores.append(final_score)

    final_scores = np.array(final_scores)
    top_positions = final_scores.argsort()[-top_n:][::-1]

    print("\n🔎 Recommended Recipes:\n")
    result=[]
    for pos in top_positions:
        idx = indices[pos]

        calories = df.loc[idx, "Calories"]
        protein = df.loc[idx, "ProteinContent"]

        # Handle missing values
        calories_display = round(calories, 1) if pd.notna(calories) else "Not Available"
        protein_display = round(protein, 1) if pd.notna(protein) else "Not Available"
        result.append({
            "name": df.loc[idx, "Name"],
            "cuisine": df.loc[idx, "Cuisine"],
            "category": df.loc[idx, "RecipeCategory"],
            "calories": calories_display,
            "protein": protein_display
        })
    return result


# ---------------------------
# CLI Interface
# ---------------------------
if __name__ == "__main__":

    print("\n=== 🍽 Smart Multi-Cuisine Recipe Recommender ===\n")

    ingredients = input("Enter ingredients (comma separated): ")

    print("\nMatch Mode:")
    print("1. Any")
    print("2. All")
    mode = "all" if input("Choose (1/2): ") == "2" else "any"

    calorie_input = input("\nMax calories? (press enter to skip): ")
    max_cal = int(calorie_input) if calorie_input else None

    protein_mode = input("High protein only? (yes/no): ")
    high_protein = protein_mode.lower() == "yes"

    print("\nProcessing...\n")

    recommend_by_ingredients(
        ingredients,
        match_mode=mode,
        max_calories=max_cal,
        high_protein=high_protein
    )