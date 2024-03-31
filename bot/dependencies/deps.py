from bot.services import PymongoService
from bot.config import MONGO
from pymongo import MongoClient


mongodb = PymongoService(client=MongoClient(MONGO))
