import pandas as pd
import numpy as np
print("Loading datasets...")

# -----------------------
# Load Western dataset
# -----------------------
df1 = pd.read_csv("data/clean_recipes.csv")

df1 = df1[[
    "Name",
    "ingredients_cleaned",
    "Calories",
    "ProteinContent",
    "RecipeCategory"
]]

# -----------------------
# Load Indian dataset
# -----------------------
ind_df = pd.read_csv("data/indian_food.csv")

# Rename columns to match structure
ind_df = ind_df.rename(columns={
    "name": "Name",
    "ingredients": "ingredients_cleaned",
    "course": "RecipeCategory"
})

# Add missing columns
ind_df["Calories"] = np.nan
ind_df["ProteinContent"] = np.nan

# Keep only required columns
ind_df = ind_df[[
    "Name",
    "ingredients_cleaned",
    "Calories",
    "ProteinContent",
    "RecipeCategory"
]]

# -----------------------
# Merge both datasets
# -----------------------
df = pd.concat([df1, ind_df], ignore_index=True)

df = df.dropna(subset=["ingredients_cleaned"])
df["ingredients_cleaned"] = df["ingredients_cleaned"].astype(str)
df = df.reset_index(drop=True)

print("Datasets merged successfully.")
print("Total combined recipes:", df.shape[0])