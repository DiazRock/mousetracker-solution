# Mouse tracker web server

This is a simple web server, that does the following 

1. Track the data from the serial port associated with the mouse, and shows is in the browser
2. When left clicking, takes a picture with the webcame that stores in the [images/] folder, and
stores the position of the mouse and the data source of the image in a sql database.

**In case the tracker can read anything from the provided serial port, it prints the 
current position of the mouse.**

## How to run it
First you need to provide a .env file in the root path of the project with the following values:

SERIAL_PORT
SERVER_PORT
SERVER_HOST

```bash
chmod +=x ./setup.sh
./setup.sh
```

## Requirements

Python 3.12
