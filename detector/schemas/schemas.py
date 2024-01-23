from typing import List, Optional
from pydantic import BaseModel


class InputImages(BaseModel):
    user_id: Optional[int] = None
    images: List[str]
