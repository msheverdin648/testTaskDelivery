import ormar
from typing import Optional, List
from datetime import datetime
from db import metadata, database

class MainMeta(ormar.ModelMeta): #Вынес настройки базы данных для моделей в отдельный класс
    metadata = metadata
    database = database


class Answer(ormar.Model):
    #Модель ответа на отзыв
    class Meta(MainMeta):
        tablename = 'Answers'
        
    
    id: str = ormar.String(max_length=255, primary_key=True)
    text: str = ormar.String(max_length=3000)
    created_at: datetime = ormar.DateTime()


class Review(ormar.Model):
    #Модель отзыва
    class Meta(MainMeta):
        tablename = 'Reviews'

    id: str = ormar.String(max_length=255, primary_key=True)
    answers: Optional[List[Answer]] = ormar.ManyToMany(Answer)
    author: str = ormar.String(max_length=255)
    body: str = ormar.String(max_length=3000)
    rated: datetime = ormar.DateTime()
    icon: str = ormar.String(max_length=255, default='😊', choices=['😖', '😊'])