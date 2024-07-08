import threading
import uvicorn
import os
import dep_container
from fastapi import FastAPI, WebSocket, Depends
from starlette.responses import FileResponse 
from schemas.point import Point
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from utils.init_db import create_tables



load_dotenv()
app = FastAPI()
mouseListener = dep_container.get_listener([])
imageCapturer = dep_container.get_image_capturer()
logger = dep_container.get_logger()


@app.get("/")
def get():
    logger.info("Serving main view page")
    return FileResponse('./frontend/index.html')


@app.post("/lclick")
async def liclick(
                point: Point,
                session: Session = Depends(dep_container.get_db)):
    logger.info(f"Received left click at {point}")
    image_path = imageCapturer.capture_image()
    point.data_source_img = image_path
    _service = dep_container.get_point_and_image_service(session)
    _service.create(point)
    logger.info(f"Image captured at {point}")
    return image_path


@app.on_event("startup")
def on_startup() -> None:
    """
    Initializes the database tables when the application starts up.
    """
    create_tables()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    mouseListener.add_client(websocket)
    logger.info("Connection accepted")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Data received from websocket, {data}")
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        logger.error(f"Connection error: {e}")
    finally:
        mouseListener.remove_client(websocket)
        logger.info(f"Connection closed in {websocket.url}")

if __name__ == "__main__":
    threading.Thread(target=mouseListener.start_mouse_listener, daemon=True).start()
    
    uvicorn.run(app, host=os.getenv("SERVER_HOST"), port=int(os.getenv("SERVER_PORT")))
