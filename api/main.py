import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response


app = FastAPI(
    title='txanalytics-api',
    description='txanalytics-api app.',
    version='0.01'
)
app.add_middleware(
    CORSMiddleware, allow_methods=['OPTIONS', 'GET', 'POST'],
    allow_origins=['*'], allow_headers=['*'],
)
app.debug = True


@app.get('/health_check')
def health_check():
    return Response('OK')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)