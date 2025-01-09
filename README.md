# **Blog REST API**

A simple Blog REST API built with Flask and SQLAlchemy that supports user authentication, CRUD operations for blog posts, and pagination.

---

## **Features**

- User Authentication:
  - Registration
  - Login
  - Logout
- Blog Post Management:
  - Create, Read, Update, Delete (CRUD) blog posts
- Pagination API for displaying multiple blog posts
- Display all blog posts and a single blog post
- Built using Flask and SQLAlchemy ORM
- JWT Authentication
- PostgreSQL  

---

## **Installation**

### **Prerequisites**
- Python 3.8 or higher
- `pip` (Python package manager)

   ### ** Set Up Virtual Environment**
 - python -m venv venv
- source venv/bin/activate 

## **Initialize the Database**
- Run the following commands to create database tables:

  - flask shell
- from app import db
- db.create_all()
- flask run --port=8080


 # **API Endpoints**

## **Authentication**

| Endpoint      | Method | Description         | Payload                                                          |
|---------------|--------|---------------------|------------------------------------------------------------------|
| `/register`   | POST   | User Registration   | `{"username": "manmohan", "email": "manmohan@gmail.com", "password": "1234"}` |
| `/login`      | POST   | User Login          | `{"email": "manmohan@gmail.com", "password": "1234"}`             |

---

## **Blog Posts**

| Endpoint       | Method | Description         | Payload                                                         |
|----------------|--------|---------------------|-----------------------------------------------------------------|
| `/posts`       | POST   | Create Blog Post    | `{"title": "New Post", "content": "This is a blog post."}`      |
| `/posts`       | GET    | Get All Posts       | Query params: `?page=1&per_page=5`                              |
| `/posts/1`     | GET    | Get Single Post     | None                                                            |
| `/posts/1`     | PUT    | Update Blog Post    | `{"title": "Updated Title", "content": "Updated content."}`     |
| `/posts/1`     | DELETE | Delete Blog Post    | None                                                            |
| `/logout`      | POST   | User Logout         | None                                                            |