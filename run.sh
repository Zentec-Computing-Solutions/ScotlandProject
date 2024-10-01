#!/bin/bash

# Function to check if a package is installed
is_package_installed() {
  python -c "import pkg_resources; pkg_resources.require('$1')" &>/dev/null
}

# Function to install dependencies from requirements.txt
install_requirements() {
  if [ -f "requirements.txt" ]; then
    echo "Checking dependencies..."
    while read -r line; do
      package=$(echo "$line" | cut -d'=' -f1) # Get the package name
      if ! is_package_installed "$package"; then
        echo "$package is not installed. Installing..."
        pip install "$line" # Install the package with its version
      else
        echo "$package is already installed."
      fi
    done <requirements.txt
  else
    echo "requirements.txt not found!"
    deactivate
    exit 1
  fi
}

# Check if virtual environment exists, if not create it and install requirements
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
  source venv/bin/activate
  install_requirements
else
  source venv/bin/activate
fi

# Check if the "repair" argument was passed to the script
if [ "$1" == "repair" ]; then
  echo "Running repair to check/install requirements..."
  install_requirements
fi

# Run the Python script (replace script.py with your script name)
python webapp/main.py

# Deactivate the virtual environment
deactivate
