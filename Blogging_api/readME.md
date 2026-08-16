# Blogging API

A production-structured REST API built with FastAPI, PostgreSQL, Redis caching, and Cloudinary image uploads — with a fully functional HTML/CSS/JS frontend.

## Features

- JWT Authentication (register, login)
- Full blog post CRUD with publish/draft system
- Comments and likes system
- Pagination and filtering
- Redis caching for public endpoints
- Cloudinary image uploads for post cover images
- Security headers middleware
- CORS configuration
- Responsive frontend (no framework)

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy
- **Auth:** JWT (python-jose)
- **Caching:** Redis
- **Image Storage:** Cloudinary
- **Validation:** Pydantic v2
- **Password Hashing:** Bcrypt
- **Frontend:** HTML, CSS, JavaScript

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
│ ├── cache.py
│ └── cloudinary.py
├── api/v1/
│ ├── router.py
│ └── endpoints/
│ ├── auth.py
│ └── blog.py
├── frontend/
│ ├── templates/
│ │ ├── index.html
│ │ ├── auth.html
│ │ ├── feed.html
│ │ ├── post.html
│ │ ├── create.html
│ │ ├── edit.html
│ │ └── dashboard.html
│ └── static/
│ ├── css/
│ │ ├── base.css
│ │ ├── landing.css
│ │ ├── auth.css
│ │ ├── feed.css
│ │ ├── post.css
│ │ ├── create.css
│ │ └── dashboard.css
│ └── js/
│ └── api.js
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
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 5. Run Redis server
```bash
redis-server
```

### 6. Run the API
```bash
uvicorn Blogging_api.main:app --reload
```

### 7. Visit the app
http://localhost:8000

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
| POST | `/api/v1/blog/posts/{id}/image` | Upload cover image | Yes |

### Comments
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/v1/blog/comments/{post_id}` | Add comment | Yes |
| GET | `/api/v1/blog/posts/{post_id}/comments` | Get comments | No |

### Likes
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/v1/blog/likes/{post_id}` | Like a post | Yes |

## Frontend Pages

| Page | URL | Auth Required |
|---|---|---|
| Landing | `/` | No |
| Auth | `/auth` | No |
| Feed | `/feed` | No |
| Post View | `/post/{id}` | No |
| Create Post | `/create` | Yes |
| Edit Post | `/edit/{id}` | Yes |
| Dashboard | `/dashboard` | Yes |

## Interactive Docs

Swagger UI available at `http://localhost:8000/docs`
