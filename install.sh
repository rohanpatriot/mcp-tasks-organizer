#!/bin/bash
# Installation script for MCP Tasks Organizer

# Check for Python 3.10+
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher is required. Found Python $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install package in development mode
echo "Installing MCP Tasks Organizer..."
pip install -e .

echo "Installation complete! MCP Tasks Organizer is ready to use."
echo ""
echo "To use with Claude for Desktop, edit your claude_desktop_config.json file."
echo "See the README.md for details." 