from fastapi import FastAPI

app = FastAPI()


@app.get("/fibonacci")
async def fibonacci_index(input: int):
    """_summary_

    Args:
        input (int): _description_

    Returns:
        _type_: _description_
    """
    return {"data": 5}
