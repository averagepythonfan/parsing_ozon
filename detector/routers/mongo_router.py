from typing import Annotated, List
from fastapi import APIRouter, Depends

from detector.schemas import MongoArticles
from detector.services import PymongoService
from detector.dependencies import get_mongo_service


router = APIRouter(
    prefix="/mongo",
    tags=['Mongo']
)


@router.post("/exists")
async def check_if_exist_in_mongo(
    data: MongoArticles,
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
):
    return mongo.check_if_exist(articles=data.articles, ozon=data.ozon)


@router.post("/add_to_unparsed")
async def add_to_unparsed(
    data: MongoArticles,
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
):
    return mongo.update_unparsed_articles(articles=data.articles, ozon=data.ozon)


@router.post("/update_parsed")
async def update_parsed(
    data: MongoArticles,
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
):
    """Add articles to parsed, pull from unparsed"""

    return mongo.update_parsed_articles(articles=data.articles, ozon=data.ozon)


@router.get("/random_unparsed")
async def update_parsed(
    ozon: bool,
    mongo: Annotated[PymongoService, Depends(get_mongo_service)],
):
    return mongo.random_unparsed(ozon=ozon)
