from fastapi import FastAPI
from detector.routers import model_router, mongo_router


app = FastAPI()
app.include_router(router=model_router)
app.include_router(router=mongo_router)
