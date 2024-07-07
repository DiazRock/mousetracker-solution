from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse
from readMouse import readMouse


app = FastAPI()


@app.get("/")
async def get():
    return FileResponse('./frontend/index.html')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            position = next(readMouse())
            await websocket.send_text(str(position))
    except Exception as e:
        print(f"Connection closed: {e}")
        await websocket.close()