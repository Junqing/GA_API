import logging
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from .models import Fibonacci, Blacklist, FibonacciOut
from .exceptions import UndefinedException
from .exceptions import ValueTooLargeException, ValueErrorException
from fastapi_pagination import add_pagination, paginate
from .pagination import Page

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s :: %(levelname)s :: %(message)s'
)

app = FastAPI()


fibonacci = Fibonacci()
blacklist = Blacklist()


@app.get("/fibonacci/{input}", response_model=FibonacciOut)
async def fibonacci_index(input: int):
    try:
        value = fibonacci.recursive(input)
        logging.debug(fibonacci.cache)
        if value not in blacklist.cache:
            return FibonacciOut(n=input, value=value)
        else:
            raise ValueError('Requested value is blacklisted')
    except RecursionError as re:
        logging.error(re)
        try:
            # Resursion has limitation, revert to use non-resursive solution
            value = fibonacci.non_resursive(input)
            logging.debug(fibonacci.cache)
            return FibonacciOut(n=input, value=value)
        except ValueError as ve:
            logging.error(ve)
            raise ValueTooLargeException(ve.args)
    except ValueError as ve:
        logging.error(ve)
        raise ValueErrorException(ve.args)
    except Exception as e:
        # Uncatched errors, investigate to refine code
        logging.error(e)
        raise UndefinedException


@app.get("/fibonacci/sequence/{input}", response_model=Page[FibonacciOut])
async def fibonacci_sequence(input: int):
    # TODO current version is naive filter for blacklist,
    # this can affect the output of total per page, should consider rearrange the pagination
    try:
        data = []
        for n in range(input):
            value = fibonacci.recursive(n)
            if value not in blacklist.cache:
                data.append(FibonacciOut(n=n, value=value))

        logging.debug(fibonacci.cache)
        return paginate(data)

    except RecursionError as re:
        logging.error(re)
        try:
            # Resursion has limitation, revert to use non-resursive solution
            for n in range(input):
                value = fibonacci.non_resursive(n)
                if value not in blacklist.cache:
                    data.append(FibonacciOut(n=n, value=value))
            logging.debug(fibonacci.cache)
            return paginate(data)
        except ValueError as ve:
            logging.error(ve)
            raise ValueTooLargeException
    except ValueError as ve:
        logging.error(ve)
        raise ValueErrorException(ve)
    except Exception as e:
        logging.error(e)
        raise UndefinedException

add_pagination(app)


@app.post("/fibonacci/blacklist/{input}", status_code=201)
async def add_blacklist(input: int):
    # input may or may not be a fibonacci number
    # checking any input might require unneccesary caching of fibonacci numbers
    if input < 0:
        raise ValueErrorException("Input is smaller than 0")
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
        raise ValueErrorException("Input is smaller than 0")
    try:
        blacklist.remove(input)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logging.error(e)
        raise UndefinedException
