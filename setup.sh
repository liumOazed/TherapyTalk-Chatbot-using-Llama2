#!/bin/bash

# Stop on first error
set -e

# Check if running as root, if not, suggest using sudo
if [ "$(id -u)" != "0" ]; then
    echo "This script may require root permissions. Please run as root or use sudo."
    exit 1
fi

echo "Installing necessary Python packages from requirements.txt..."
pip3.10 install -r requirements.txt

echo "Downloading the spaCy English model..."
python3.10 -m spacy download en_core_web_sm

echo "Setup completed successfully."