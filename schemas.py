from pydantic import BaseModel
from datetime import datetime

class Review(BaseModel):

    answers: list
    author: str
    body: str
    rated: datetime