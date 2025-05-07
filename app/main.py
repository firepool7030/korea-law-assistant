from fastapi import FastAPI
from routers import law_meta

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello World"

app.include_router(law_meta.router)

