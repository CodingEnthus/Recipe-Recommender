# 🍳 Smart Recipe AI

**Smart Recipe AI** is an AI-powered web application that recommends recipes based on the ingredients a user has available.
It combines **Natural Language Processing (NLP), Machine Learning, FastAPI, and a modern frontend** to create an intelligent cooking assistant.

Users can enter ingredients, apply filters like calories or protein preference, and instantly receive recipe suggestions.

---

# 🚀 Features

* 🔐 **User Authentication**

  * Signup and Login system
  * Password hashing using **bcrypt**
  * User data stored in **MongoDB Atlas**

* 🤖 **AI Recipe Recommendation**

  * Ingredient-based recipe search
  * Uses **TF-IDF + Cosine Similarity**
  * Supports **Global + Indian recipes**

* 🥗 **Smart Filters**

  * Match **Any / All ingredients**
  * **Maximum calorie** filter
  * **High protein mode**

* 🧠 **Text Processing**

  * Ingredient normalization
  * Lemmatization using **NLTK**
  * Ingredient synonym mapping

* 🌐 **Modern Web Interface**

  * Futuristic **AI kitchen themed UI**
  * Animated **fridge login screen**
  * Responsive **recipe cards**

* ⚡ **FastAPI Backend**

  * RESTful APIs
  * High performance asynchronous server

---

# 🏗️ Project Architecture

```
Frontend (HTML + CSS + JS)
        ↓
FastAPI Backend
        ↓
Machine Learning Recommendation Model
        ↓
MongoDB Atlas (User Authentication)
```

---

# 📂 Project Structure

```
AI Project
│
├── frontend
│   ├── login.html
│   ├── dashboard.html
│   ├── style.css
│   ├── dashboard.css
│   ├── script.js
│   └── dashboard.js
│
├── api
│   ├── main.py
│   ├── database.py
│
├── model
│   └── recommender.py
│
├── data
│   ├── clean_recipes.csv
│   └── indian_food.csv
│
└── README.md
```

---

# 🧠 Machine Learning Model

The recommendation engine uses:

### TF-IDF Vectorization

Converts ingredient text into numerical vectors.

### Cosine Similarity

Measures similarity between the user's ingredients and recipes.

### Scoring Strategy

```
Final Score =
0.7 × Ingredient Similarity
+ 0.25 × Ingredient Overlap
+ Cuisine Boost
```

This helps recommend recipes that closely match the user’s available ingredients.

---

# 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Scikit-learn
* NLTK
* MongoDB Atlas
* PyMongo
* Passlib (bcrypt)

### Frontend

* HTML
* CSS
* JavaScript

### Machine Learning

* TF-IDF Vectorizer
* Cosine Similarity
* NLP preprocessing

---

# ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/smart-recipe-ai.git
cd smart-recipe-ai
```

---

### 2️⃣ Create virtual environment

```
python -m venv venv
```

Activate:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```
pip install fastapi uvicorn scikit-learn nltk pymongo passlib[bcrypt]
```

---

### 4️⃣ Run the API server

```
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

# 📡 API Endpoints

### User Authentication

**Signup**

```
POST /signup
```

```
{
  "email": "user@email.com",
  "password": "password123"
}
```

---

**Login**

```
POST /login
```

```
{
  "email": "user@email.com",
  "password": "password123"
}
```

---

### Recipe Recommendation

```
POST /recommend
```

Example request:

```
{
  "ingredients": "chicken rice butter",
  "match_mode": "any",
  "max_calories": 400,
  "high_protein": false
}
```

---

# 🎯 Future Improvements

* 🤖 AI Chat Chef
* 🖼️ Recipe Image Generation
* 📸 Ingredient Detection using Computer Vision
* 🗣️ Voice-based ingredient input
* 📅 Weekly Meal Planner
* ⭐ Favorite Recipes system
* 🥗 Nutrition score prediction
* ☁️ Cloud deployment

---

# 👨‍💻 Author

**Samrat Dutta**

Python Developer | AI & Backend Enthusiast

---

# ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute!
