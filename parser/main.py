from fastapi import FastAPI
from parser.routers import router


app = FastAPI()

app.include_router(router=router)