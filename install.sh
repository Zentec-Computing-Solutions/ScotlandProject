#!/bin/bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Reset
Color_Off='\033[0m' # Text Reset

# Regular Colors
Red='\033[0;31m'    # Red
Green='\033[0;32m'  # Green
Yellow='\033[0;33m' # Yellow
Blue='\033[0;34m'   # Blue
Cyan='\033[0;36m'   # Cyan

# Function to check if a package is installed
is_package_installed() {
  python -c "import pkg_resources; pkg_resources.require('$1')" &>/dev/null
}

# Function to install dependencies from requirements.txt
install_requirements() {
  if [ -f "requirements.txt" ]; then
    printf "${Yellow}Checking dependencies...\n"
    SECONDS=0
    while read -r line; do
      package=$(printf "$line" | cut -d'=' -f1) # Get the package name
      if ! is_package_installed "$package"; then
        printf "${Yellow}$package is not installed. Installing...\n"
        pip install "$line" # Install the package with its version
      else
        printf "${Green}$package is already installed.\n"
      fi
    done <requirements.txt
    printf "${Green}Dependencies installed in %s seconds.\n" "$SECONDS"
  else
    printf "${Red}requirements.txt not found!\n"
    deactivate
    exit 1
  fi
}

# Check if virtual environment exists, if not create it and install requirements
cd "$SCRIPT_DIR"
printf "${Blue}Creating virtual enviroment...\n"
SECONDS=0
python3 -m venv --system-site-packages venv
source venv/bin/activate
printf "${Green}Virtual enviroment created in %s seconds.\n" "$SECONDS"
printf "${Cyan}Installing requirements...\n"
printf "${Cyan}This may take a minute...\n"
install_requirements

# Fix weird Picamera2 bug where it fails to install
sudo apt -y install python3-picamera2

# Fix weird numpy bug
pip uninstall numpy
pip install numpy

printf "${Cyan}Adding service to systemd...\n"
# Install and start the service
if [ -f /etc/systemd/system/kinacam.service ]; then
    sudo systemctl stop kinacam.service
    sudo systemctl disable kinacam.service
else
    sudo \cp -f ./kinacam.service /etc/systemd/system/kinacam.service
fi

sudo systemctl enable kinacam.service
sudo systemctl start kinacam.service
printf "${Green}Service added to systemd.\n"
printf "${Green}Kinacam install complete, reboot to start Kinacam.\n"

