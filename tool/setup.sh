#!/bin/bash

# Ensure Python and pip are installed
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install Python 3."
    exit 1
fi

if ! command -v pip3 &>/dev/null; then
    echo "pip is not installed. Please install pip for Python 3."
    exit 1
fi

# Define the target directory (local bin)
TARGET_DIR="$HOME/.local/bin"

# Create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Install requirements from the requirements.txt file
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip3 install --user -r requirements.txt
else
    echo "requirements.txt not found. Please make sure it's in the same directory as this script."
    exit 1
fi

# Move the Python files to the target directory
for file in *.py; do
    if [ -f "$file" ]; then
        mv "$file" "$TARGET_DIR"
        echo "Moved $(basename "$file") to $TARGET_DIR"
    fi
done

# Make the Python scripts executable
for file in "$TARGET_DIR"/*.py; do
    chmod +x "$file"
    echo "Made $(basename "$file") executable"
done

# Create a symlink for easy access (optional)
SCRIPT_NAME="twz.py"  # The main script that you want to run globally
if [ -f "$TARGET_DIR/$SCRIPT_NAME" ]; then
    ln -sf "$TARGET_DIR/$SCRIPT_NAME" "$TARGET_DIR/twz"
    echo "Created symlink 'twz' to run the tool globally."
else
    echo "Main script $SCRIPT_NAME not found."
fi

echo "Setup complete. The tool is now globally accessible."
