import dep_container
import json
from typing import List
from fastapi import WebSocket

class Publisher:
    def __init__ (self, ws_clients: List[WebSocket]):
        self.ws_clients = ws_clients
        self.logger = dep_container.get_logger()

    def add_client(self, ws_client: List[WebSocket]):
        self.ws_clients.append(ws_client)
        self.logger.info(f"New client connected")
    
    def remove_client(self, ws_client: List[WebSocket]):
        self.ws_clients.remove(ws_client)
        self.logger.info(f"Client disconnected")

    async def publish(self, data):
        read_line_data = json.dumps(data)
        for ws_client in self.ws_clients:
            self.logger.info(f"Sending data to {ws_client.url}")
            await ws_client.send_text(read_line_data)
    

        

