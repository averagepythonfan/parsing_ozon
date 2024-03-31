from bson import ObjectId
from pymongo import MongoClient


class PymongoService:


    def __init__(self, client: MongoClient) -> None:
        self.db = client.get_database(name="parse")
        self.collection = self.db.get_collection(name="pictures")
    

    def get_random_pic(self, only_yolo: bool = True) -> tuple[str, str]:
        if only_yolo:
            query = {"$match": {"human": {"$eq": None}, "tf_model": {"$eq": True}}}
        else:
            query = {"$match": {"human": {"$eq": None}}}
        random_pic = list(self.collection.aggregate([
            query,
            {"$sample": { "size": 1 }}
        ]))[0]
        return random_pic["_id"].binary.hex(), random_pic["link"]
    

    def set_human(self, obj_id: ObjectId, human: bool) -> int:
        result = self.collection.update_one(
            {"_id": obj_id},
            {"$set": {"human": human}}
        )
        return result.modified_count
    
    def stats(self) -> tuple[int, int, int]:
        humans = self.collection.count_documents({"human": True})
        no_humans = self.collection.count_documents({"human": False})
        pic_count = self.collection.count_documents({})
        return humans, no_humans, pic_count