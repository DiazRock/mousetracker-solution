import threading
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse 
import uvicorn
from mouseListener.mouseListener import MouseListener

app = FastAPI()
mouseListener = MouseListener([])


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Example</title>
    </head>
    <body>
        <h1>
            WebSocket Mouse Position
        </h1>
        <div id="position">
        </div>
        <script lang="js">
            const ws = new WebSocket("ws://" + location.host + "/ws");
        
            ws.onmessage = function(event) {
                const eventDiv = document.getElementById('events');
                const data = JSON.parse(event.data);
                if (data.type === 'move') {
                    eventDiv.innerHTML = 'Mouse moved to (' + data.x + ', ' + data.y + ')';
                } else if (data.type === 'click') {
                    const action = data.pressed ? 'pressed' : 'released';
                    eventDiv.innerHTML = 'Mouse ' + data.button + ' ' + action + ' at (' + data.x + ', ' + data.y + ')';
                } else if (data.type === 'scroll') {
                    eventDiv.innerHTML = 'Mouse scrolled at (' + data.x + ', ' + data.y + ') with delta (' + data.dx + ', ' + data.dy + ')';
                }
            };
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return FileResponse('./frontend/index.html')

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
    
    uvicorn.run(app, host="0.0.0.0", port=8005)