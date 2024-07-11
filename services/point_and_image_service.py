from typing import List, Optional
from sqlalchemy.orm import Session
from repositories.point_and_image_repository import PointAndImageRepository
from schemas.point import Point
from models.point import PointAndImage

class PointAndImageService:
    def __init__(self, session: Session):
        self.repository = PointAndImageRepository(session)

    def create(self, data: Point) -> bool:
        return self.repository.create(data)

    def get_all(self) -> List[Optional[PointAndImage]]:
        return self.repository.get_all()
