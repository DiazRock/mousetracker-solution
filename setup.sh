#!/usr/bin/bash

# Load local variables
set -a
source .env
set +a

# Make the image directory
mkdir $STATIC_FOLDER/images

# Install virtualenv using pip
pip install virtualenv

# Create a virtual environment named 'venv'
virtualenv venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements from the requirements.txt file
pip install -r requirements.txt

# Run the fapi.py server
python fapi.py

