from fastapi import FastAPI
from routers import laws

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello World"

app.include_router(laws.router)

