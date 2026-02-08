# Masterblog API

A simple yet complete **RESTful Blog API** built with **Flask**, including a lightweight frontend, full CRUD functionality, search & sorting, and interactive API documentation via **Swagger UI**.

This project was created as a learning exercise to understand how backend APIs, frontend JavaScript, and documentation work together in a real-world setup.

---

## ✨ Features

### Backend (Flask API)

* List all blog posts (`GET /api/posts`)
* Create a new post (`POST /api/posts`)
* Update an existing post (`PUT /api/posts/<id>`)
* Delete a post (`DELETE /api/posts/<id>`)
* Search posts across title, content, author, and date
* Sort posts by `title`, `content`, `author`, or `date` (ascending / descending)
* Input validation and proper HTTP status codes

### Blog Post Model

Each post contains:

```json
{
  "id": 1,
  "title": "My Post",
  "content": "Post content",
  "author": "Author name",
  "date": "YYYY-MM-DD"
}
```

### Frontend

* Simple HTML/CSS/JavaScript frontend
* Fetches data from the API
* Displays blog posts
* Add and delete posts via UI

## 🧠 Data Storage

> **Important note:**  
> This project currently uses **in-memory storage**.

All blog posts are stored in a Python list (`POSTS`) inside the backend application.
This means:

- Data is **not persisted**
- All posts are lost when the backend server restarts
- No database or JSON file is used intentionally

This approach was chosen to keep the focus on:
- REST API design
- HTTP methods and status codes
- Request validation
- Search and sorting logic
- Frontend–backend interaction

---


### API Documentation

* Interactive Swagger UI available at:

  ```
  http://127.0.0.1:5002/api/docs
  ```

---

## 📁 Project Structure

```
Masterblog-API/
│
├── backend/
│   ├── backend_app.py        # Flask API
│   └── static/
│       └── masterblog.json   # Swagger definition
│
├── frontend/
│   ├── templates/
│   │   └── index.html        # Frontend HTML
│   └── static/
│       ├── main.js           # Frontend JavaScript
│       └── styles.css        # Styling
│
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/markL1391/Masterblog-API.git
cd Masterblog-API
```

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install flask flask-cors flask-swagger-ui
```

### 4️⃣ Run the backend

```bash
python backend/backend_app.py
```

The API will run on:

```
http://127.0.0.1:5002
```

### 5️⃣ Open the frontend

Open the file below in your browser:

```
frontend/templates/index.html
```

Make sure the API base URL is set to:

```
http://127.0.0.1:5002/api
```

---

## 🔍 API Usage Examples

### Get all posts

```
GET /api/posts
```

### Create a post

```
POST /api/posts
```

```json
{
  "title": "New Post",
  "content": "Hello World",
  "author": "Mark",
  "date": "2026-02-08"
}
```

### Update a post

```
PUT /api/posts/1
```

### Delete a post

```
DELETE /api/posts/1
```

### Search posts

```
GET /api/posts?search=flask
```

### Sort posts

```
GET /api/posts?sort=date&direction=desc
```

---

## 🧠 Notes

* Data is stored **in-memory** (no database)
* Restarting the server resets the posts
* Designed for learning purposes, not production

---

## 📌 Possible Extensions

* Persist data using SQLite or PostgreSQL
* Add user authentication
* Likes & comments
* Pagination
* Deployment (Docker / Railway / Render)

---

## 👤 Author

Created by **Mark** as part of a Flask & API learning journey 🚀

---

Happy coding! 🎉
