from fastapi import FastAPI
import uvicorn

from db import database, metadata, engine
from api import parser_router


app = FastAPI() #Инициализация приложения

#---------------------------------------------------------------
#Подключение и настройка базы данных


metadata.create_all(engine)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


#-----------------------------------------------------------------
app.include_router(parser_router)#Подключение роутера




if __name__ == '__main__':

    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)