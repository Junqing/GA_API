import logging
from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .responses import BaseResponse, PaginatedResponse
from .models import Fibonacci, Blacklist
from .exceptions import NegativeIntegerException, UndefinedException
from .exceptions import BlacklistException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s :: %(levelname)s :: %(message)s'
)

app = FastAPI()

fibonacci = Fibonacci()
blacklist = Blacklist()


@app.get("/fibonacci/{input}")
async def fibonacci_index(input: int):
    try:
        if input >= 0:
            value = fibonacci(input)
            logging.debug(fibonacci.cache)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"data": value}
            )
        else:
            raise NegativeIntegerException
    except Exception as e:
        # Uncatched errors, investigate to refine code
        logging.error(e)
        raise UndefinedException


@app.get("/fibonacci/sequence/{input}")
async def fibonacci_sequence(input: int, page: int, pagesize: int = 100):
    try:
        if input > 0:
            data = [fibonacci(n) for n in range(input)]
            logging.debug(fibonacci.cache)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"data": data}
            )
        raise NegativeIntegerException
    except Exception as e:
        logging.error(e)
        raise UndefinedException


@app.post("/fibonacci/blacklist/{input}", status_code=201)
async def add_blacklist(input: int):
    # input may or may not be a fibonacci number
    # checking any input might require unneccesary caching of fibonacci numbers
    try:
        if input < 0:
            raise NegativeIntegerException
        elif input in blacklist.cache:
            raise BlacklistException(
                detail="Input {x} is already in the blacklist".format(x=input))
        else:
            blacklist.add(input)
            logging.debug(blacklist.cache)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"data": "ok"}
            )
    except Exception as e:
        logging.error(e)
        raise UndefinedException


@app.delete("/fibonacci/blacklist/undo/{input}", status_code=200)
async def remove_blacklist(input: int):
    try:
        if input < 0:
            raise NegativeIntegerException
        elif input not in blacklist.cache:
            raise BlacklistException(
                detail="Input {x} not in blacklist".format(x=input))
        else:
            blacklist.remove(input)
            return JSONResponse(status_code=status.HTTP_200_OK)
    except Exception as e:
        logging.error(e)
        raise UndefinedException
