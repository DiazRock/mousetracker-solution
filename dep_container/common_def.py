import logging
from deviceCommunicators.mouseEventTracker import MouseEventTracker
from deviceCommunicators.imageCapturer import ImageCapturer
from functools import lru_cache
from deviceCommunicators.publisher import Publisher
from repositories.point_and_image_repository import PointAndImageRepository
from sqlalchemy.orm import Session
from services.point_and_image_service import PointAndImageService


def get_mouse_event_tracker(publisher):
    return MouseEventTracker(publisher)


def get_publisher(clients):
    return Publisher(clients)


def get_image_capturer():
    return ImageCapturer


@lru_cache(maxsize=None)
def get_logger():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

    
def get_point_and_image_repository(session: Session):
    return PointAndImageRepository(session)

def get_point_and_image_service(session: Session):
    return PointAndImageService(session)

