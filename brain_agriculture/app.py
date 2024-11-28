from http import HTTPStatus

from fastapi import FastAPI

from brain_agriculture.routers import users, auth, farmers
from brain_agriculture.schemas import Message


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(farmers.router)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
