from model import Todo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


# app obj

app = FastAPI()

from database import (
        fetch_one_todo,
        fetch_all_todos, 
        create_todo,
        update_todo, 
        remove_todo,
)

origins = ['http://localhost:3000']

app.add_middleware(
        CORSMiddleware, 
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
)

@app.get("/")
def root():
    return {"Ping": 'pong'}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title):  
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is not TODO item with this title! {title}")

@app.post("/api/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.model_dump())
    if response:
        return response
    raise HTTPException(400, "Bad request!")

@app.put("/api/todo/{title}")
async def update_todo(title:str, desc:str):
    response = await update_todo(title, desc)
    if response:
        return response

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {title}")
