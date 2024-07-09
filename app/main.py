from fastapi import FastAPI, HTTPException
import uvicorn
from app.api.routers.clientsRouter import client_router
from app.api.routers.usersRouter import user_router
from app.db.init_db import init_db

app = FastAPI()

init_db()

app.include_router(client_router, prefix='/clients', tags=['clients'])
app.include_router(user_router, prefix='/users', tags=['users'])

@app.get('/')
async def root():
    return {'message': 'Estudo - construindo uma aplicação FastAPI'}