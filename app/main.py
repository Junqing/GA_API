import logging
from fastapi import FastAPI
from .utils import fibonacci_of_func

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s :: %(levelname)s :: %(message)s'
)

app = FastAPI()


@app.get("/fibonacci/{input}")
async def fibonacci_index(input: int):
    return {"data": fibonacci_of_func(input)}


@app.get("/fibonacci/sequence/{input}")
async def fibonacci_sequence(input: int, page: int, pagesize: int = 100):
    return {"data": [5]}


@app.post("/fibonacci/blacklist/{input}")
async def add_blacklist(input: int):
    return {"ok"}


@app.delete("/fibonacci/blacklist/undo/{input}")
async def remove_blacklist(input: int):
    return {"ok"}
