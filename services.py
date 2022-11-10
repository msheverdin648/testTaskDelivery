import requests
import asyncio
import aiohttp
import json

    
def get_total(): #Функция получения общего числа отзывов
    url = 'https://api.delivery-club.ru/api1.2/reviews?chainId=48274&limit=1&offset=0&cacheBreaker=1668100117'
    response = requests.get(url=url)
    response_json = response.json()
    total = response_json['total']
    return total


async def get_data(session, url, offset):


    async with session.get(url=url) as response:
        response_json = await response.json()

        with open(f'jsons/{offset}.json', 'w') as jsonfile:
            json.dump(response_json, jsonfile, ensure_ascii=False)



async def start_parser(): #Управляющая функция парсера
    
    #Парсить начинаем с первого отзыва пачками по 3500шт.
    offset = 0  #С какойого отзыва начинаем парсить
    step = 3500
    total = get_total()
    tasks = [] #Список заданий на парсинг
    async with aiohttp.ClientSession() as session:
        while True:
            print(offset)
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
        
        await asyncio.gather(*tasks)
#total = 35613
#step = 3500
#offse = 35000
#step = total-postiton = 613


if __name__ == '__main__':
    asyncio.run(start_parser())