import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from config import (
    DEBUG, ALLOWED_ORIGINS
)
from routers import transactions
from storages import initialize_users_storage
from storages import initialize_transactions_storage


app = FastAPI(
    title='txanalytics-api',
    version='1.0',
    description='''
    This is an API documentation for listing banking transactions that happened 
    on different payment accounts during the last 2 years. 
    ''',

)
app.add_middleware(
    CORSMiddleware, allow_methods=['OPTIONS', 'GET', ],
    allow_origins=ALLOWED_ORIGINS,
)
app.debug = DEBUG
app.include_router(
    transactions.router,
    prefix='/api/v1/transactions'
)


@app.on_event("startup")
async def startup_event():
    initialize_users_storage()
    initialize_transactions_storage()


@app.get('/health_check')
def health_check():
    return Response('OK')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
