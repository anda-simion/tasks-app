# 🧩 Tasks App

A simple full-stack **task management** application built with:

- **FastAPI** (backend)
- **React** (frontend)
- **PostgreSQL** (database)
- **Docker & Docker Compose** (container orchestration)

---

## 🚀 Project Overview

This app allows you to create, list, and manage tasks.  
The frontend communicates with the backend API to interact with a PostgreSQL database.

**Architecture:**

```
frontend (React) → backend (FastAPI) → PostgreSQL (db)
```

---

## 🧰 Tech Stack

- **Frontend:** React (CRA)
- **Backend:** FastAPI (Python 3.11)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy + asyncpg
- **Containerization:** Docker Compose

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/tasks-app.git
cd tasks-app
```

### 2️⃣ Environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://tasks_user:tasks_password@db:5432/tasks_db
REACT_APP_API_URL=http://localhost:8000
```

### 3️⃣ Build and run with Docker

```bash
docker-compose up --build
```

This will:

- start the **PostgreSQL** database
- run the **FastAPI backend** on port **8000**
- run the **React frontend** on port **3000**

Visit the app at 👉 [http://localhost:3000](http://localhost:3000)

---

## 🧩 Development

To run services locally without Docker:

### Backend

```bash
cd backend
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm start
```

Make sure PostgreSQL is running on your system or Docker.

---

## 📦 Project Structure

```
tasks-app/
│
├── backend/              # FastAPI app
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── ...
│
├── frontend/             # React app
│   ├── src/
│   └── package.json
│
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

---

## 🧹 Useful Commands

- Stop all containers:
  ```bash
  docker-compose down
  ```
- Rebuild everything:
  ```bash
  docker-compose up --build -d
  ```
- View logs:
  ```bash
  docker-compose logs -f
  ```

---

## 🪪 License

This project is open-source under the **MIT License**.
