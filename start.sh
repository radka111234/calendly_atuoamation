#!/bin/bash

# Install Google Chrome
apt-get update
apt-get install -y wget gnupg2 curl
curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get -f install
apt-get install -y chromium

# Run the Python script
python main.py
