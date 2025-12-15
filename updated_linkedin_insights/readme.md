
# LinkedIn Insights Microservice

A **FastAPI-based backend microservice** that collects and serves insights for LinkedIn company pages.  
The service focuses on **backend architecture, data modeling, and clean API design** rather than real-time LinkedIn scraping.  

It uses a **dummy scraper layer** that returns deterministic sample data and stores it in a **MySQL** database through **SQLAlchemy ORM**.  
Users can query company pages, their posts, comments, and followers using REST endpoints.

---

## 🧩 Key Features

- **FastAPI REST API** with multiple endpoints for LinkedIn page insights.  
- **MySQL database** integration via **SQLAlchemy ORM**.  
- **Core entities:** Page, Post, Comment, Employee.  
- **Dummy scraper layer (`scraper.py`)** that generates consistent fake data to simulate LinkedIn responses.  
- **DB-first approach** — data is fetched from the database first; the scraper is used only if data is missing.  
- **Filtering and pagination** support for listing pages by:
  - Partial **name** match
  - **Industry** type
  - **Follower count** range  
- Clean and modular project structure designed for scalability.

---

## ⚙️ Tech Stack

- **Python 3.10+**  
- **FastAPI** (web framework)  
- **SQLAlchemy ORM**  
- **MySQL** (relational database)  
- **Uvicorn** (ASGI development server)

---

## 📁 Project Structure

```
linkedin_insights/
├─ app/
│  ├─ __init__.py
│  ├─ main.py          # FastAPI entry point
│  ├─ database.py      # SQLAlchemy engine & session
│  ├─ models.py        # ORM models
│  ├─ schemas.py       # Pydantic schemas
│  ├─ scraper.py       # Dummy LinkedIn scraper
│  ├─ crud.py          # Database CRUD operations
│  ├─ utils.py         # Pagination & helper utilities
│  └─ routers/
│     ├─ __init__.py
│     └─ pages.py      # Page-related routes
├─ requirements.txt
├─ .env
└─ README.md
```

---

## 🚀 Setup and Installation

### 1. Clone the repository
```
git clone <your-repo-url>.git
cd linkedin_insights
```

### 2. Create and activate a virtual environment
```
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/macOS
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root and add your database URL:
```
DATABASE_URL=mysql+pymysql://<db_user>:<db_password>@localhost:3306/linkedin_insights
```

Ensure that the database **linkedin_insights** exists.  
SQLAlchemy will automatically create all tables on startup.

---

## 🖥️ Running the Server

Start the development server with:
```
uvicorn app.main:app --reload
```

Access interactive documentation at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 Core Endpoints

### 1. Get Page Details
Fetch metadata and insights for a specific LinkedIn page.  
If the page isn’t in the database, it’s fetched from the dummy scraper and stored.

```
GET /pages/{page_id}
```

**Example:**
```
GET /pages/deepsolv
```

**Returns:**  
Page details, followers, posts, comments, and employee info.

---

### 2. List Pages with Filters and Pagination
Retrieve a filtered list of LinkedIn pages.

```
GET /pages?name=deep&industry=Technology&min_followers=1000&max_followers=50000&page=1&limit=10
```

**Supported query parameters:**
- `name` – Partial page name match  
- `industry` – Industry filter  
- `min_followers` / `max_followers` – Follower range  
- `page`, `limit` – Pagination controls  

---

### 3. Get Recent Posts
Fetch recent posts for a given company page.

```
GET /pages/{page_id}/posts?limit=10
```

**Example:**
```
GET /pages/deepsolv/posts?limit=10
```

**Returns:**  
Posts ordered by most recent first.

---

### 4. Get Followers (Dummy Data)
Fetch simulated follower details for a given page using dummy data.

```
GET /pages/{page_id}/followers?limit=20
```

**Example:**
```
GET /pages/deepsolv/followers?limit=20
```

---

## 🧠 Development Notes

- The `scraper.py` file simulates a LinkedIn data fetcher using **controlled, static data**.  
- This approach ensures safety and compliance with LinkedIn’s **terms of service**.  
- The scraper can later be **replaced** with:
  - LinkedIn’s official API (with proper permissions)  
  - An internal or third-party data provider  

The rest of the codebase (DB models, APIs, CRUD, and pagination) will work unchanged.

---

## 🚫 Why No Real LinkedIn Scraping?

- **LinkedIn prohibits automated access and scraping** of its platform.  
- Including real scraping logic in public code would **violate their terms of service**.  
- The purpose of this project is to focus on **backend system design, ORM modeling, and API development**, not bypassing platform restrictions.

---

## 💡 What This Project Demonstrates

- Clean and modular backend architecture  
- Relational database modeling with SQLAlchemy  
- RESTful API design with pagination and filtering  
- Integration-ready scraper abstraction pattern  

---

## 🏁 Summary

The **LinkedIn Insights Microservice** demonstrates how to design and build a scalable backend service that aggregates and serves company insights using modern Python tools while maintaining clean separation of layers, compliance, and extendability.






