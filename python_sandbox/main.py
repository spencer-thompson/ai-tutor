import logging

from fastapi import FastAPI
from IPython.core.interactiveshell import InteractiveShell
from pydantic import BaseModel

app = FastAPI()

logger = logging.getLogger("uvicorn")


class Block(BaseModel):
    """
    A code block
    """

    code: str


class Wrapper(BaseModel):
    json: Block


@app.post("/execute")
def execute_code(content: Wrapper):
    """
    Execute and return a given code block
    """
    try:
        result = InteractiveShell.instance().run_cell(content.json.code).result
    except ModuleNotFoundError as e:
        logger.error(e)

    return result
