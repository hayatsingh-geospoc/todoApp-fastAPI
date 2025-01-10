# Todo Application with FastAPI and Streamlit

A simple Todo application built with FastAPI backend, MongoDB database, and Streamlit frontend.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your MongoDB connection details:

```
MONGODB_URL="your_mongodb_connection_string"
DATABASE_NAME="todo_db"
```

## Running the Application

1. Start the FastAPI backend:

```bash
uvicorn app.backend.main:app --reload
```

2. In a new terminal, start the Streamlit frontend:

```bash
streamlit run app/frontend/streamlit_app.py
```

The application will be available at:

- Backend API: http://localhost:8000
- Frontend: http://localhost:8501

## Features

- Create new todos with title and description
- Mark todos as complete/incomplete
- Delete todos
- Beautiful and responsive UI
- Real-time updates
