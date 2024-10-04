"""
TODO

create server to connect chat / users / personas
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/")
def login():
    return {"hello": "world"}


@app.get("/")
def logout():
    return {"hello": "world"}
