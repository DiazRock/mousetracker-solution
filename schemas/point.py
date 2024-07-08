from typing import Optional
from pydantic import BaseModel

class Point(BaseModel):
    x: float
    y: float
    data_source_img: Optional[str] = ""

