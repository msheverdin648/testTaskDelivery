from fastapi import APIRouter


parser_router = APIRouter()

@parser_router.get('/parse_reviews')
async def parse_reviews():
    return {'key': 'hello'}