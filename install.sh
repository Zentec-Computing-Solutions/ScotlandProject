#!/bin/bash

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Function to check if a package is installed
is_package_installed() {
  python -c "import pkg_resources; pkg_resources.require('$1')" &> /dev/null
}

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
  while read -r line; do
    package=$(echo "$line" | cut -d'=' -f1)  # Get the package name
    if ! is_package_installed "$package"; then
      echo "$package is not installed. Installing..."
      pip install "$line"  # Install the package with its version
    else
      echo "$package is already installed."
    fi
  done < requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

# Run the Python script (replace script.py with your script name)
python webapp/main.py

# Deactivate the virtual environment
deactivate
