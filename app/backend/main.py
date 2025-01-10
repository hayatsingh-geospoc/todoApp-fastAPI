from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .database import todo_collection
from bson import ObjectId

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Todo(TodoCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    todo_dict = todo.model_dump()
    todo_dict["created_at"] = datetime.utcnow()
    result = todo_collection.insert_one(todo_dict)
    todo_dict["id"] = str(result.inserted_id)
    return todo_dict

@app.get("/todos/", response_model=List[Todo])
async def get_todos():
    todos = []
    for todo in todo_collection.find():
        todo["id"] = str(todo.pop("_id"))
        todos.append(todo)
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str):
    todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo["id"] = str(todo.pop("_id"))
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo: TodoCreate):
    updated_todo = todo_collection.find_one_and_update(
        {"_id": ObjectId(todo_id)},
        {"$set": todo.model_dump()},
        return_document=True
    )
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo["id"] = str(updated_todo.pop("_id"))
    return updated_todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    result = todo_collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"} 