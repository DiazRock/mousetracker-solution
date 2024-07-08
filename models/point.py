from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import dep_container
import uuid


class PointAndImage(dep_container.Base):
    __tablename__ = 'PointAndImage'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_source = Column(String, nullable=False)

    # Vertical axis is the first component or the x
    x_axis = Column(Float, nullable=False)

    # Horizontal axis is the second component or the y
    y_axis = Column(Float, nullable=False)
