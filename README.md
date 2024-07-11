# Mouse tracker web server

This is a simple web server, that does the following 

1. Track the data from the movement of the mouse, and shows it in the browser
2. When left clicking, takes a picture with the webcame that stores in the [images/] folder, and
stores the position of the mouse and the data source of the image in a sql database.

## How to run it
First you need to provide a .env file in the root path of the project with the following values:

SERVER_PORT
SERVER_HOST
ELAPSED_TIME (For time between each mouse event tracked)

```bash
chmod +=x ./setup.sh
./setup.sh
```

## Checking the information in the database and the pictures source
In the folder [./images] you will see the pictures.
There is gonna be a database.db file in the root path of the project.
Load this folder inside a sqlite console and then run:

```sql
select * FROM PointAndImage;
```


## Requirements

Python 3.12
