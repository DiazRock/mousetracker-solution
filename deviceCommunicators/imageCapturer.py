import time
import cv2
import os


class ImageCapturer:

    @staticmethod
    def capture_image():
        print("Capturing image")
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            return None
        img_path = f"{os.getenv('STATIC_FOLDER')}/images/{int(time.time())}.png"
        cv2.imwrite(img_path, frame)
        cam.release()
        return img_path
