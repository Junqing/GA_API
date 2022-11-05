import logging
from fastapi import FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .responses import BaseResponse, PaginatedResponse
from .models import Fibonacci, Blacklist

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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input {number} ".format(number=input) +
                "is not a positive integer")
    except Exception as e:
        # Undecided error handling
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error, investigation ongoing")


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input {number} ".format(number=input) +
            "is not a positive integer")
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error, investigation ongoing")


@app.post("/fibonacci/blacklist/{input}", status_code=201)
async def add_blacklist(input: int):
    # input may or may not be a fibonacci number
    # checking any input might require unneccesary caching of fibonacci numbers
    try:
        if input < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input {number} ".format(number=input) +
                "is not a positive integer")
        elif input in blacklist.cache:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input {number} ".format(number=input) +
                "is already in the blacklist")
        else:
            blacklist.add(input)
            logging.debug(blacklist.cache)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"data": "ok"}
            )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error, investigation ongoing")


@app.delete("/fibonacci/blacklist/undo/{input}", status_code=200)
async def remove_blacklist(input: int):
    try:
        if input < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input {number} ".format(number=input) +
                "is not a positive integer")
        elif input not in blacklist.cache:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input {number} ".format(number=input) +
                "is not in the blacklist")
        else:
            blacklist.remove(input)
            return JSONResponse(status_code=status.HTTP_200_OK)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error, investigation ongoing")
