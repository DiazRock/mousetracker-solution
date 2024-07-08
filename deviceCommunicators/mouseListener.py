import asyncio
import json
import time
import requests
import os
import dep_container
from pynput import mouse
from serial import Serial
from dotenv import load_dotenv
from fastapi import WebSocket


load_dotenv()

class DataPoint:
    def __init__(self, data) -> None:
        self.logger = dep_container.get_logger()
        self.logger.info(f"Data to send {data}")
        self._data = data
    
    @property
    def data(self):
        return self._data


class MouseListener:

    def __init__(self, clients: list) -> None:
        self.clients = clients
        self.logger = dep_container.get_logger()
        self.serial = Serial(os.getenv('SERIAL_PORT'), 9600, timeout = 1)
        pass

    def add_client(self, client: WebSocket):
        self.logger.info(f"Adding a client connection to {client.url}")
        self.clients.append(client)
    
    def remove_client(self, client: WebSocket):
        self.logger.info(f"Removing a client connection from {client.url}")
        self.clients.remove(client)

    def on_move(self, x, y):
        time.sleep(0.05)
        dataPoint = DataPoint({'type': 'move', 'x': x, 'y': y})
        asyncio.run(self.send_move_info(dataPoint.data))

    def on_click(self, x, y, button, pressed):
        time.sleep(0.05)
        dataPoint = DataPoint({'type': 'click', 'x': x, 'y': y, 'button': str(button), 'pressed': pressed})
        asyncio.run(self.send_click_info(dataPoint.data))

    async def send_click_info(self, data):
        for client in self.clients:
            self.logger.info(f"Sending mouse click position to {client.url}")
            await client.send_text(json.dumps(data))
        dataToSend = { 'x': float(data['x']), 
                       'y': float(data['y'])}
        self.logger.info(f"Storing the point position in the server {dataToSend}")
        with requests.post("http://localhost:8008/lclick", 
                           json = dataToSend) as response:
            self.logger.info(f"Response received from the server {response}")

    async def send_move_info(self, data):
        read_line_data = self.serial.readline().decode('utf-8')
        if read_line_data == '':
            self.logger.warning("The serial port lecture is empty. Sending the mouse position instead")
            read_line_data = json.dumps(data)
        for client in self.clients:
            await client.send_text(read_line_data)

    def start_mouse_listener(self):
        with mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        ) as listener:
            listener.join()

