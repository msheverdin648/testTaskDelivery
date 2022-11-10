from fastapi import APIRouter
from models import Review
from typing import List
from services import start_parser
import asyncio

# from filters import ReviewFilter


parser_router = APIRouter()




@parser_router.get('/get_all_reviews', response_model=List[Review])
async def get_all_reviews(icon: str):

    reviews = await Review.objects.all()

    return reviews


@parser_router.get('/parse_data')
def parse_data():

    asyncio.run(start_parser())
    
    return {'status': 200}