from fastapi import APIRouter, Query
from datetime import datetime
from models import Review
from typing import List
from services import start_parser
import asyncio



parser_router = APIRouter()




@parser_router.get('/reivews', response_model=List[Review])
async def get_reviews(
        page: int=Query(1, gt=0, description='page number',), 
        page_size: int=Query(20, gt=0, description='size of getting data'), 
        rating: str = Query(None, description='Filter for rating 😊 or 😖'),
        date: str = Query(None, description='Filter for date dd.mm.yyyy'),
        sorted: str = Query(None, description='Sorting for date column: rated(от старых к новым), -rated(от новых к старым)')
    ):


    #В зависимости от входных данных фильтра и сортировки делается запрос в бд
    queryset = Review.objects.paginate(page, page_size).select_related('answers')
    if rating:
        queryset = queryset.filter(icon=rating)
    if date:
        filter_date = datetime.strptime(date, '%d.%m.%Y')
        queryset = queryset.filter(rated__icontains=filter_date.date())
    if sorted:
        queryset = queryset.order_by(f"{sorted}")

    return await queryset.all()




@parser_router.get('/parse_data')
def parse_data():

    asyncio.run(start_parser())
    
    return {'status': 200}



