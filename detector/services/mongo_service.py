from typing import List
from pymongo import MongoClient
from detector.schemas import Picture


class PymongoService:

    def __init__(self, client: MongoClient) -> None:
        self.ozon = client.get_database(name="ozon")
        self.wb = client.get_database(name="wb")
        # self.collection = self.db.get_collection(name="pictures")
        # self.articles = self.db.get_collection(name="articles")

    def add_pic(self, link: str = None, yolo: bool = None, article: int = None, ozon: bool = False):
        pic = Picture(link=link, yolo=yolo, article=article)
        pic.define_vid()
        pics = self.ozon.get_collection(name="pictures") if ozon else self.wb.get_collection(name="pictures")
        result = pics.insert_one(pic.model_dump(exclude_none=True))
        return result.acknowledged


    def check_if_exist(self, articles: List[int], ozon: bool = False) -> dict:
        return_dict = dict()
        db_articles = self.ozon.get_collection(name="articles") if ozon else self.wb.get_collection(name="articles")
        for el in articles:
            exist = len(list(db_articles.find(
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
    

    def update_unparsed_articles(self, articles: List[int], ozon: bool = False) -> dict:
        db_articles = self.ozon.get_collection(name="articles") if ozon else self.wb.get_collection(name="articles")
        unparsed = db_articles.update_one(
            {"name": "not parsed articles"},
            {"$addToSet": {"articles": {"$each": articles}}},
            upsert=True
        )
        return unparsed.modified_count

    def update_parsed_articles(self, articles: List[int], ozon: bool = False) -> dict:
        db_articles = self.ozon.get_collection(name="articles") if ozon else self.wb.get_collection(name="articles")
        parsed = db_articles.update_one(
            {"name": "parsed articles"},
            {"$addToSet": {"articles": {"$each": articles}}},
            upsert=True
        )

        unparsed = db_articles.update_one(
            {"name": "not parsed articles"},
            {"$pull": {"articles": {"$in": articles}}}
        )

        return {
            "parsed update": parsed.modified_count,
            "unparsed update": unparsed.modified_count,
        }


    def random_unparsed(self, ozon: bool = False) -> int:
        db_articles = self.ozon.get_collection(name="articles") if ozon else self.wb.get_collection(name="articles")
        not_parsed = db_articles.find_one({"name": "not parsed articles"})
        if not_parsed:
            not_parsed_arts = not_parsed["articles"]
            return not_parsed_arts[0] if len(not_parsed_arts) != 0 else "there is not unparsed articles"
        else:
            return "there is not unparsed articles"
