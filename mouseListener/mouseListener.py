import asyncio
import json
from pynput import mouse
import time
import requests
from serial import Serial

class MouseListener:

    def __init__(self, clients: list) -> None:
        self.clients = clients
        self.serial = Serial('/dev/input/mouse2', 9600, timeout = 1)
        pass
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        print("Data to send ", value)
        self._data = value

    def add_client(self, client):
        print("Adding a client")
        self.clients.append(client)
    
    def remove_client(self, client):
        print("Removing a client")
        self.clients.remove(client)

    def on_move(self, x, y):
        time.sleep(0.05)
        self.data = {'type': 'move', 'x': x, 'y': y}
        asyncio.run(self.send_to_clients())

    def on_click(self, x, y, button, pressed):
        time.sleep(0.05)
        self.data = {'type': 'click', 'x': x, 'y': y, 'button': str(button), 'pressed': pressed}
        asyncio.run(self.send_click_info(self.data))

    async def send_click_info(self, data):
        dataToSend = { 'x': int(data['x']), 
                       'y': int(data['y']), 
                       'data_source_img': "foo"}
        print(dataToSend)
        with requests.post("http://localhost:8008/lclick", 
                           json = dataToSend) as response:
            print("The response ", response)

    async def send_to_clients(self):
        self.data = str(self.serial.readline())
        for client in self.clients:
            await client.send_text(self.data)

    def start_mouse_listener(self):
        with mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        ) as listener:
            listener.join()

