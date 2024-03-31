from typing import List
from pymongo import MongoClient
from detector.schemas import Picture


class PymongoService:

    def __init__(self, client: MongoClient) -> None:
        self.db = client.get_database(name="parse")
        self.collection = self.db.get_collection(name="pictures")
        self.articles = self.db.get_collection(name="articles")

    def add_pic(self, link: str = None, yolo: bool = None, article: int = None):
        pic = Picture(link=link, yolo=yolo, article=article)
        pic.define_vid()
        result = self.collection.insert_one(pic.model_dump(exclude_none=True))
        return result.acknowledged


    def check_if_exist(self, articles: List[int]) -> dict:
        return_dict = dict()
        for el in articles:
            exist = len(list(self.articles.find(
                {
                    "articles": {"$exists": True, "$in": [el]},
                    "name": "parsed articles"
                },
                {
                    "_id": 1
                }
            )))
            return_dict[el] = True if exist == 1 else False 
        return return_dict
    
    def update_parsed_articles(self, articles: List[int]) -> dict:
        parsed = self.articles.update_one(
            {"name": "parsed articles"},
            {"$addToSet": {"articles": {"$each": articles}}}
        )

        unparsed = self.articles.update_one(
            {"name": "not parsed articles"},
            {"$pull": {"articles": {"$in": articles}}}
        )

        return {
            "parsed update": parsed.modified_count,
            "unparsed update": unparsed.modified_count,
        }


    def random_unparsed(self) -> int:
        not_parsed = self.articles.find_one({"name": "not parsed articles"})["articles"]
        return not_parsed[0]
