from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class InputImages(BaseModel):
    user_id: Optional[int] = None
    images: List[str]
    article: int


class Picture(BaseModel):
    article: int
    link: str
    vid: Optional[bool] = None
    yolo: Optional[bool] = None
    human: Optional[bool] = None
    date: datetime = datetime.now()

    def define_vid(self):
        if "video" in self.link:
            self.vid = True
        else:
            self.vid = False
