#!/bin/bash

VENV_DIR=".venv"

if ! command -v python3.10 &> /dev/null; then
    echo "Python 3.10 could not be found. Please install it first."
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3.10 -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists."
fi

echo "Installing packages..."
# Activate and install packages in a subshell to avoid polluting current shell
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "requirements.txt not found. Please create one using: pip freeze > requirements.txt"
  exit 1
fi

#echo "Setup complete. Please activate your environment with:"
echo "source $VENV_DIR/bin/activate"
