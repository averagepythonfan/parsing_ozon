from pymongo import MongoClient
from detector.services import ModelService, PymongoService
from detector.config import MONGO


def get_model_service():
    return ModelService()


def get_mongo_service():
    mongo = MongoClient(MONGO)
    return PymongoService(client=mongo)
