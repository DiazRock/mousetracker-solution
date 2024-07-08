import dep_container
from models.point import PointAndImage


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    PointAndImage.metadata.create_all(bind=dep_container.engine)

