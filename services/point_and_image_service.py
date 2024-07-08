from typing import List, Optional
from sqlalchemy.orm import Session
from repositories.point_and_image_repository import PointAndImageRepository
from schemas.point import Point


class PointAndImageService:
    def __init__(self, session: Session):
        self.repository = PointAndImageRepository(session)

    def create(self, data: Point) -> bool:
        return self.repository.create(data)

    def get_all(self) -> List[Optional[Point]]:
        return self.repository.get_all()
