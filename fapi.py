import threading
import uvicorn
import os
import dep_container
import asyncio
import json
from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse 
from schemas.point import Point
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from utils.init_db import create_tables


load_dotenv()
app = FastAPI()
publisher = dep_container.Publisher([])
mouseEventTracker = dep_container.get_mouse_event_tracker(publisher)
imageCapturer = dep_container.get_image_capturer()
logger = dep_container.get_logger()


@app.get("/")
def get():
    logger.info("Serving main view page")
    return FileResponse('./frontend/index.html')

@app.on_event("startup")
def on_startup() -> None:
    """
    Initializes the database tables when the application starts up.
    """
    create_tables()


async def lclick(
                point: Point,
                session: Session):
    logger.info(f"Received left click at {point}")
    image_path = imageCapturer.capture_image()
    point.data_source_img = image_path
    _service = dep_container.get_point_and_image_service(session)
    _service.create(point)
    logger.info(f"Image captured at {point}")
    return image_path


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    publisher.add_client(websocket)
    logger.info("Connection accepted")
    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            logger.info(f"Data received from websocket: {data}")
            if data['event'] == 'lclick':
                logger.info("Received left click event")
                db_session = next(dep_container.get_db())
                await lclick(Point(x=data['x'], y=data['y']), session=db_session)
            asyncio.sleep(os.getenv('ELAPSED_TIME'))

    except Exception as e:
        logger.error(f"Connection error: {e}")
    finally:
        publisher.remove_client(websocket)
        logger.info(f"Connection closed in {websocket.url}")


if __name__ == "__main__":
    threading.Thread(target=mouseEventTracker.start_mouse_listener, daemon=True).start()
    uvicorn.run(app, host=os.getenv("SERVER_HOST"), port=int(os.getenv("SERVER_PORT")))
