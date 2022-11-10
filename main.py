from fastapi import FastAPI
from api import parser_router

app = FastAPI()

app.include_router(parser_router)