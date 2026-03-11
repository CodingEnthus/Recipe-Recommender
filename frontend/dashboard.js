document.addEventListener("DOMContentLoaded", () => {

const searchBtn = document.getElementById("searchBtn");
const resultsDiv = document.getElementById("results");

searchBtn.addEventListener("click", async () => {

    const ingredients = document.getElementById("ingredients").value;
    const matchMode = document.getElementById("matchMode").value;
    const maxCalories = document.getElementById("maxCalories").value;
    const highProtein = document.getElementById("highProtein").checked;

    if (!ingredients) {
        alert("Please enter ingredients");
        return;
    }

    resultsDiv.innerHTML = "AI Chef is cooking... 🍳";

    try {

        const response = await fetch("http://127.0.0.1:8000/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ingredients: ingredients,
                match_mode: matchMode,
                max_calories: maxCalories ? parseInt(maxCalories) : null,
                high_protein: highProtein
            })
        });

        const data = await response.json();

        resultsDiv.innerHTML = "";

        if (!data.results || data.results.length === 0) {
            resultsDiv.innerHTML = "<p>No recipes found 😔</p>";
            return;
        }

        data.results.forEach(recipe => {

            const card = document.createElement("div");
            card.classList.add("recipe-card");

            card.innerHTML = `
                <h3>🍽 ${recipe.name}</h3>
                <p>🌍 <b>Cuisine:</b> ${recipe.cuisine}</p>
                <p>📂 <b>Category:</b> ${recipe.category}</p>
                <p>🔥 <b>Calories:</b> ${recipe.calories}</p>
                <p>💪 <b>Protein:</b> ${recipe.protein}</p>
            `;

            resultsDiv.appendChild(card);

        });
        resultsDiv.scrollIntoView({behavior:"smooth"});

    } catch (error) {
        console.error(error);
        resultsDiv.innerHTML = "<p>Error connecting to AI Kitchen ⚠️</p>";
    }

});

});