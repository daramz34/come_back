# AI Recipe Generator API

An AI-powered recipe generation backend built with FastAPI and Google Gemini API. 
Users describe what they're craving, and the AI suggests meals and generates 
detailed recipes — with a focus on Nigerian and African cuisine.

## About This Project

This is my 4th project this week. The entire backend was designed and built by me 
from scratch, including the database architecture, API structure, Gemini integration, 
and authentication system.

For the frontend, I used VS Code Copilot to implement it — my main goal with this 
project was to deepen my backend and AI integration skills, not frontend development. 
I needed a way to interact with the API, but I've since realized I don't need to build 
a whole frontend just to test a backend.

Going forward I'll be using **Postman** to test my API endpoints directly — a cleaner 
and more professional approach to API development and testing.

---

## Features

- JWT Authentication (register, login)
- Mood/craving-based meal suggestions via Gemini AI
- Multiple meal options — decline and get new suggestions
- Full recipe generation (ingredients, steps, tips)
- Cuisine filter (Nigerian, Italian, Asian, etc.)
- Dietary preference support (halal, vegan, keto, etc.)
- Cooking time filter
- Save and manage recipe history
- Mark recipes as favourites
- Rate recipes (1–5 stars)
- Production-structured FastAPI project

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy
- **AI:** Google Gemini API (gemini-1.5-flash)
- **Auth:** JWT (python-jose)
- **Validation:** Pydantic v2
- **Password Hashing:** Bcrypt
- **Frontend:** HTML, CSS, JavaScript (VS Code Copilot assisted)

## Project Structure

Recipe_api/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
├── core/
│ ├── config.py
│ ├── security.py
│ └── dependencies.py
├── api/v1/
│ ├── router.py
│ └── endpoints/
│ ├── auth.py
│ └── recipes.py
├── services/
│ └── gemini.py
└── .env


## Setup

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd Recipe_api
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```env
DATABASE_URL=postgresql://username:password@localhost/recipe_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Run the API
```bash
uvicorn Recipe_api.main:app --reload
```

### 6. Visit Swagger docs
http://localhost:8000/docs

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Register user | No |
| POST | `/api/v1/auth/login` | Login | No |

### Recipes
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/v1/recipes/suggest` | Get AI meal suggestions | Yes |
| POST | `/api/v1/recipes/generate` | Generate full recipe | Yes |
| GET | `/api/v1/recipes/history` | Get recipe history | Yes |
| GET | `/api/v1/recipes/favourites` | Get favourite recipes | Yes |
| GET | `/api/v1/recipes/{id}` | Get single recipe | Yes |
| PATCH | `/api/v1/recipes/{id}` | Rate or favourite recipe | Yes |
| DELETE | `/api/v1/recipes/{id}` | Delete recipe | Yes |

## How It Works
User describes craving + sets filters (cuisine, dietary, cooking time)
↓
Gemini suggests 5 meal options
↓
User picks one meal from the suggestions
↓
Gemini generates full recipe with ingredients, steps, and tips
↓
Recipe saved to user's history
↓
User can rate, favourite, or delete recipes


## Author

Oluwadarasimi Rotimi  
GitHub: https://github.com/daramz34  
LinkedIn: https://www.linkedin.com/in/oluwadarasimi-rotimi-40007a420/
