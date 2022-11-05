from fastapi import FastAPI

app = FastAPI()


@app.get("/fibonacci/{input}")
async def fibonacci_index(input: int):
    return {"data": 5}


@app.get("/fibonacci/{input}")
async def fibonacci_sequence(input: int, page: int, pagesize: int = 100):
    return {"data": [5]}


@app.post("/fibonacci/{input}")
async def add_blacklist(input: int):
    return {"ok"}


@app.delete("/fibonacci/{input}")
async def remove_blacklist(input: int):
    return {"ok"}
