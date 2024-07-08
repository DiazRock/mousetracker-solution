from pydantic import BaseModel


class Point(BaseModel):
    x: int
    y: int
    data_source_img: str