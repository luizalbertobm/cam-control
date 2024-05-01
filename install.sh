#!/usr/bin/bash

# sudo apt update
sudo apt install -y python3 v4l-utils
sudo cp camera-control.png /usr/share/icons/
sudo cp camera-control.desktop /usr/share/applications/
sudo cp camera-control.py /usr/local/bin/camerac
sudo chmod +x /usr/local/bin/camerac

echo "Installation complete"