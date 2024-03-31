from typing import Annotated, List
from fastapi import APIRouter, Depends

from detector.services import PymongoService
from detector.dependencies import get_mongo_service


router = APIRouter(
    prefix="/mongo",
    tags=['Mongo']
)


@router.get("/exists")
async def check_if_exist(
    articles: List[int],
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
):
    return mongo.check_if_exist(articles=articles)


@router.post("/update_parsed")
async def update_parsed(
    articles: List[int],
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
):
    return mongo.update_parsed_articles(articles=articles)


@router.get("/random_unparsed")
async def update_parsed(
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
):
    return mongo.random_unparsed()
