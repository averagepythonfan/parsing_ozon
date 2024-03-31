import re
import asyncio
import random
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from playwright.async_api import async_playwright as pl
from parser.schemas import ParseObject
from parser.services import ParserService
from parser.dependencies import get_parser


router = APIRouter(
    prefix="/parser",
    tags=["Parser"]
)


@router.post("/article")
async def parse(
    product: ParseObject,
    parser: Annotated[ParserService, Depends(get_parser)],
):
    async with parser() as browser:
        browser: ParserService
        await browser.parse(article=product.article, user_id=product.user_id)
        if await browser.return_links():
            return {"message": "all links send to detector"}
        else:
            raise HTTPException(
                status_code=432,
                detail="Detector not found"
            )
