import threading
from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse 
import uvicorn
import dep_container
from models.point import Point

app = FastAPI()
mouseListener = dep_container.get_listener([])


@app.get("/")
async def get():
    return FileResponse('./frontend/index.html')

@app.post("/lclick")
async def liclick(point: Point):
    return point


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    mouseListener.add_client(websocket)
    try:
        while True:
            print("Before receiving information")
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        mouseListener.remove_client(websocket)

if __name__ == "__main__":
    threading.Thread(target=mouseListener.start_mouse_listener, daemon=True).start()
    
    uvicorn.run(app, host="0.0.0.0", port=8008)