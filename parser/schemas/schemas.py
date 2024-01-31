from pydantic import BaseModel


class ParseObject(BaseModel):
    user_id: int
    article: int
