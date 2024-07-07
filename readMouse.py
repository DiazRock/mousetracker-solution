from serial import Serial
import time


def readMouse():
    try:
        print("Starting the reading")
        with Serial('/dev/input/mouse0', 9600, timeout=1) as serial:
            while True:
                line = serial.readline().decode('utf-8').strip()
                #print("Line ", line)

                if line and line.startswith("X:") and "Y:" in line:
                    yield line
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Serial connection closed")

