import re
import asyncio
import random
from typing import Annotated
from fastapi import APIRouter, Depends
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
        await browser.parse(product.article)
        return browser.return_links()
