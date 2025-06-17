#!/bin/bash

# Exit if any command fails
set -e
set -x  # Debug mode: shows commands as they run

# Install dependencies
pip install -r requirements.txt

# Run the app using Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:8000 app:app
