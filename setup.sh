#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y tesseract-ocr

# Install Python dependencies
pip install -r requirements.txt
