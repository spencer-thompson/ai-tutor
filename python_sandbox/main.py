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


@app.post("/execute")
def execute_code(content: Block):
    """
    Execute and return a given code block
    """
    try:
        result = InteractiveShell.instance().run_cell(content.code).result
    except ModuleNotFoundError as e:
        logger.error(e)

    return result
