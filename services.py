import requests
import asyncio
import aiohttp
from ormar.exceptions import NoMatch 
import json
from datetime import datetime


from models import Review, Answer
    
def get_total(): #Функция получения общего числа отзывов
    url = 'https://api.delivery-club.ru/api1.2/reviews?chainId=48274&limit=1&offset=0&cacheBreaker=1668100117'
    response = requests.get(url=url)
    response_json = response.json()
    total = response_json['total']
    return total


async def get_data(session, url, offset):


    async with session.get(url=url) as response:
        response_json = await response.json()
        return response_json



async def start_parser(): #Управляющая функция парсера
    
    #Парсить начинаем с первого отзыва пачками по 3500шт.
    offset = 0  #С какойого отзыва начинаем парсить
    step = 3500
    total = get_total()
    tasks = [] #Список заданий на парсинг
    async with aiohttp.ClientSession() as session:
        while True:
            if offset+step > total and offset < total: #Проверка не выходим ли за значения общего числа
                #Если выходим то считаем сколько осталось и добавляем последнее задание и выходим из цикла
                step = total-offset
                url = f'https://api.delivery-club.ru/api1.2/reviews?chainId=48274&limit={step}&offset={offset}'
                task = asyncio.create_task(get_data(session, url, offset)) 
                tasks.append(task)
                break

            url = f'https://api.delivery-club.ru/api1.2/reviews?chainId=48274&limit={step}&offset={offset}'
            task = asyncio.create_task(get_data(session, url, offset)) 
            tasks.append(task)

            offset += step
        
        data = await asyncio.gather(*tasks)

        for item in data:
            for review in item['reviews']:
                review_data = {
                    'id': review['orderHash'],
                    'author': review['author'],
                    'body': review['body'],
                    'rated': datetime.strptime(review['rated'], "%Y-%m-%dT%H:%M:%S%z"),
                    'icon': review['icon']
                }
                review_object = await create_review(review_data=review_data)
                for answer in review['answers']:
                    answer_data = {
                        'id': answer['publicUuid'],
                        'text': answer['answer'],
                        'created_at': datetime.strptime(answer['createdAt'], "%Y-%m-%dT%H:%M:%S%z"),
                    }
                    answer_object = await create_answer(answer_data)
                    await review_object.answers.add(answer_object)

        return data


async def create_review(review_data):
    try:
        review_object = await Review.objects.update_or_create(
            id=review_data['id'], 
            author=review_data['author'],
            body=review_data['body'],
            rated=review_data['rated'],
            icon=review_data['icon']
        ) 
    except NoMatch:
        review_object = await Review.objects.create(
            id=review_data['id'], 
            author=review_data['author'],
            body=review_data['body'],
            rated=review_data['rated'],
            icon=review_data['icon']
        ) 
    return review_object

async def create_answer(answer_data):
    try:
        answer_object = await Answer.objects.update_or_create(
            id=answer_data['id'], 
            text=answer_data['text'], 
            created_at=answer_data['created_at']
        )
    except NoMatch:
        answer_object = await Answer.objects.create(
            id=answer_data['id'],
            text=answer_data['text'], 
            created_at=answer_data['created_at']
        )
    return answer_object
            



if __name__ == '__main__':
    asyncio.run(start_parser())