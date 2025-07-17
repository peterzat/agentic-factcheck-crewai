#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: ./fact-check.sh \"<topic>\""
  echo "Example: ./fact-check.sh \"latest AI developments\""
  exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script's directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
  echo "Error: Virtual environment not found at $SCRIPT_DIR/.venv"
  echo "Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# Activate virtual environment and run the script
source .venv/bin/activate
python news_checker.py "$1" 