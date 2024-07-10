"""
This module defines the MouseListener class, which detects 
the positon and the click event of the mouse, using the pynput package
"""

import asyncio
import dep_container.common_def as common_def
from pynput import mouse
from dotenv import load_dotenv

load_dotenv()


class MouseEventTracker:

    def __init__(self, publisher) -> None:
        self.logger = common_def.get_logger()
        self.publisher = publisher

    def on_move(self, x, y):
        dataPoint = {'type': 'move', 'x': x, 'y': y}
        asyncio.run(self.publisher.publish(dataPoint))

    def on_click(self, x, y, button, pressed):
        dataPoint = {'type': 'click', 'x': x, 'y': y, 'button': str(button), 'pressed': pressed}
        asyncio.run(self.publisher.publish(dataPoint))

    def start_mouse_listener(self):
        with mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        ) as listener:
            self.logger.info("Started to listen for mouse events")
            listener.join()

