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

# Initialize fibonacci and blacklist
fibonacci = Fibonacci()
blacklist = Blacklist()


@app.get("/fibonacci/{input}", response_model=FibonacciOut)
async def fibonacci_index(input: int):
    """Endpoint that returns the value
    from the Fibonacci sequence for a given number.

    Args:\n
        input (int): Positive integer from 0 to ~900.
        Input above 900 will cause error due to the number being too large

    Raises:\n
        ValueError: Error caused by input value
        ValueTooLargeException: Value is too large
        ValueErrorException:
            Value can be blacklisted,
            Value shouldn't be negative
        UndefinedException: Uncaught errors, will need further investigation

    Returns:\n
        _type_: application/json
    """
    try:
        value = fibonacci.recursive(input)
        logging.debug(fibonacci.cache)
        if value not in blacklist.cache:
            return FibonacciOut(n=input, value=value)
        else:
            raise ValueError("Requested value is blacklisted")
    except RecursionError as re:
        logging.error(re)
        try:
            # Resursion has limitation, revert to use non-resursive solution
            value = fibonacci.non_resursive(input)
            logging.debug(fibonacci.cache)
            return FibonacciOut(n=input, value=value)
        except ValueError as ve:
            logging.error(ve)
            raise ValueTooLargeException()
    except ValueError as ve:
        logging.error(ve)
        raise ValueErrorException(ve.args)
    except Exception as e:
        # Uncatched errors, investigate to refine code
        logging.error(e)
        raise UndefinedException


@app.get("/fibonacci/sequence/{input}", response_model=Page[FibonacciOut])
async def fibonacci_sequence(input: int):
    """Endpoint that returns a list of numbers and the
    corresponding values from the Fibonacci sequence
    from 1 to N with support for pagination.
    Page size should be parameterized with a default of 100.

    Args:\n
        input (int): input (int): Positive integer larger than 1.
        Input too large will cause error due to the number being too large
        (Only when pagination is pointing at those large numbers)

    Raises:\n
        ValueError: Error caused by input value
        ValueTooLargeException: Value is too large
        ValueErrorException:
            Value can be blacklisted,
            Value shouldn't be negative
        UndefinedException: Uncaught errors, will need further investigation

    Returns:\n
        _type_: application/json
    """
    # TODO current version is naive filter for blacklist,
    # this result in less page size,
    # should consider rearrange pagination
    if input < 1:
        raise ValueErrorException("Input must be larger than 0")
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
    """Endpoint to blacklist a number to permanently stop it
    from being shown in Fibonacci results when requested.
    The blacklisted numbers should persist in application state.

    Args:\n
        input (int): A positive integer wished to be blacklisted,
        even if the number is not a fibonacci number it will still be accepted

    Raises:\n
        ValueErrorException: Input should not be smaller than 0
        UndefinedException: Uncaught errors, will need further investigation

    Returns:\n
        _type_: application/json
    """
    if input < 0:
        raise ValueErrorException("Input is smaller than 0")
    try:
        blacklist.add(input)
        logging.debug(blacklist.cache)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"data": f"{input} is blacklisted"}
        )
    except Exception as e:
        logging.error(e)
        raise UndefinedException


@app.delete("/fibonacci/blacklist/undo/{input}", status_code=204)
async def remove_blacklist(input: int):
    """Endpoint to remove a number from the blacklist.

    Args:\n
        input (int): A positive integer that should be removed from blacklist

    Raises:\n
        ValueErrorException: 
            Value should not be smaller than 0
            Not is not found in the blacklist
        UndefinedException: Uncaught errors, will need further investigation

    Returns:\n
        _type_: none
    """
    if input < 0:
        raise ValueErrorException("Input is smaller than 0")
    try:
        blacklist.remove(input)
        return None
    except ValueError as ve:
        raise ValueErrorException(ve.args)
    except Exception as e:
        logging.error(e)
        raise UndefinedException
