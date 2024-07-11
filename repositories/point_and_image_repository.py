from typing import List, Optional
from sqlalchemy.orm import Session
from models.point import PointAndImage
from schemas.point import Point


class PointAndImageRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: Point) -> bool:
        pointAndImage = PointAndImage(
                        x_axis = data.x,
                        y_axis = data.y,
                        image_source = data.data_source_img)
        self.session.add(pointAndImage)
        self.session.commit()
        self.session.refresh(pointAndImage)
        return True

    def get_all(self) -> List[Optional[PointAndImage]]:
        print(self.session.query(PointAndImage).all())
        return self.session.query(PointAndImage).all()
