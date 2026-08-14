# Blogging API

A production-structured REST API built with FastAPI, PostgreSQL, and Redis caching.

## Features

- JWT Authentication (register, login)
- Full blog post CRUD with publish/draft system
- Comments and likes system
- Pagination and filtering
- Redis caching for public endpoints
- Security headers middleware
- CORS configuration

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy
- **Auth:** JWT (python-jose)
- **Caching:** Redis
- **Validation:** Pydantic v2
- **Password Hashing:** Bcrypt

## Project Structure
Blogging_api/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
├── core/
│ ├── config.py
│ ├── security.py
│ ├── dependencies.py
│ └── cache.py
├── api/v1/
│ ├── router.py
│ └── endpoints/
│ ├── auth.py
│ └── blog.py
└── .env

## Setup

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd Blogging_api
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
DATABASE_URL=postgresql://username:password@localhost/blog_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379
```

### 5. Run Redis server
```bash
redis-server
```

### 6. Run the API
```bash
uvicorn Blogging_api.main:app --reload
```

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Register user | No |
| POST | `/api/v1/auth/login` | Login | No |

### Posts
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/blog/posts` | Get all published posts | No |
| GET | `/api/v1/blog/posts/mine` | Get my posts | Yes |
| GET | `/api/v1/blog/posts/{id}` | Get post by ID | No |
| POST | `/api/v1/blog/posts` | Create post | Yes |
| PUT | `/api/v1/blog/posts/{id}` | Update post | Yes |
| PATCH | `/api/v1/blog/posts/{id}` | Publish post | Yes |
| DELETE | `/api/v1/blog/posts/{id}` | Delete post | Yes |

### Comments
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/v1/blog/comments/{post_id}` | Add comment | Yes |
| GET | `/api/v1/blog/posts/{post_id}/comments` | Get comments | No |

### Likes
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/v1/blog/likes/{post_id}` | Like a post | Yes |

## Interactive Docs

Swagger UI available at `http://localhost:8000/docs`