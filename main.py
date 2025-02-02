from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel, EmailStr

import uvicorn

app = FastAPI()


class CreateUser(BaseModel):
    email: EmailStr


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!"
    }


@app.post("/users")
def create_user(user: CreateUser):
    return {
        "message": "success",
        "email": user.email
    }


@app.post("/calc/add")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result" : a + b,
    }





@app.get("/hello") 
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}





if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)