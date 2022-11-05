import logging
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .responses import BaseResponse, PaginatedResponse
from .models import Fibonacci

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s :: %(levelname)s :: %(message)s'
)

app = FastAPI()

fibonacci = Fibonacci()


@app.get("/fibonacci/{input}")
async def fibonacci_index(input: int):
    if not isinstance(input, int):
        input = int(input)

    value = fibonacci(input)
    logging.debug(fibonacci.cache)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": value}
    )


@app.get("/fibonacci/sequence/{input}")
async def fibonacci_sequence(input: int, page: int, pagesize: int = 100):
    data = [fibonacci(n) for n in range(input)]
    logging.debug(fibonacci.cache)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": data}
    )


@app.post("/fibonacci/blacklist/{input}", status_code=201)
async def add_blacklist(input: int):
    return {"ok"}


@app.delete("/fibonacci/blacklist/undo/{input}", status_code=201)
async def remove_blacklist(input: int):
    return {"ok"}
