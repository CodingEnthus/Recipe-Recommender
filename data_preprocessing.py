import pandas as pd

print("Loading dataset...")

df = pd.read_parquet("data/recipes.parquet")
df = df.head(50000)

# Keep only needed columns
columns_needed = [
    "RecipeId",
    "Name",
    "RecipeIngredientParts",
    "RecipeCategory",
    "Calories",
    "ProteinContent",
    "CarbohydrateContent",
    "FatContent"
]

df = df[columns_needed]

# Drop missing values
df = df.dropna()

# Convert ingredient list to string
df["ingredients_cleaned"] = df["RecipeIngredientParts"].apply(
    lambda x: " ".join([i.lower().strip() for i in x])
)

print("After Cleaning Shape:", df.shape)
print("\nSample cleaned ingredients:\n", df["ingredients_cleaned"].iloc[0])

# Save cleaned dataset
df.to_csv("data/clean_recipes.csv", index=False)

print("\nClean dataset saved.")
