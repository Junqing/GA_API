import logging
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from .models import FibonacciByRecursion, FibonacciNoRecursion, Blacklist
from .exceptions import NegativeIntegerException, UndefinedException
from .exceptions import ValueTooLargeException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s :: %(levelname)s :: %(message)s'
)

app = FastAPI()

fibonacci = FibonacciByRecursion()
fibonacci2 = FibonacciNoRecursion()
blacklist = Blacklist()


@app.get("/fibonacci/{input}")
async def fibonacci_index(input: int):
    try:
        value = fibonacci.recursive(input-1)
        logging.debug(fibonacci.cache)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": value}
        )
    except RecursionError as re:
        logging.error(re)
        try:
            # Resursion has limitation, revert to use non-resursive solution
            value = fibonacci.non_resursive(input-1)
            logging.debug(fibonacci.cache)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"data": value}
            )
        except ValueError as ve:
            logging.error(ve)
            raise ValueTooLargeException
    except ValueError as ve:
        logging.error(ve)
        raise NegativeIntegerException
    except Exception as e:
        # Uncatched errors, investigate to refine code
        logging.error(e)
        raise UndefinedException


@app.get("/fibonacci/sequence/{input}")
async def fibonacci_sequence(input: int, page: int, pagesize: int = 100):
    try:
        data = [fibonacci(n) for n in range(input)]
        logging.debug(fibonacci.cache)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": data}
        )
    except ValueError as ve:
        logging.error(ve)
        raise NegativeIntegerException
    except RecursionError as re:
        logging.error(re)
        raise ValueTooLargeException
    except Exception as e:
        logging.error(e)
        raise UndefinedException


@app.post("/fibonacci/blacklist/{input}", status_code=201)
async def add_blacklist(input: int):
    # input may or may not be a fibonacci number
    # checking any input might require unneccesary caching of fibonacci numbers
    if input < 0:
        raise NegativeIntegerException
    try:
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
    if input < 0:
        raise NegativeIntegerException
    try:
        blacklist.remove(input)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        raise UndefinedException
