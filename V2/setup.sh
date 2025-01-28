#!/bin/bash
# Create and activate virtual environment
python -m venv L-IRC-V2
source L-IRC-V2/bin/activate

# Install dependencies
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
