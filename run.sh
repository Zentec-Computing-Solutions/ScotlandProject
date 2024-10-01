#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  # Create the virtual environment
  python3 -m venv venv

  # Activate the virtual environment
  source venv/bin/activate

  # Run the Python script (replace script.py with your script name)
  python webapp/main.py

  # Deactivate the virtual environment
  deactivate
else
  # Run the install script if the virtual environment exists
  ./install.sh
fi
