#!/bin/bash

# Ensure we're running the script as a normal user, not root
if [ "$(id -u)" -eq 0 ]; then
    echo "Please do not run the script as root. Run it as a normal user."
    exit 1
fi

# Get the current directory (where the script is being run from)
CURRENT_DIR=$(pwd)

# Install the required Python dependencies
echo "Installing dependencies from requirements.txt..."
pip install --user -r "$CURRENT_DIR/requirements.txt"

# Set up the alias in the user's .bashrc or .zshrc file
USER_HOME=$(eval echo ~$USER)

if [ -f "$USER_HOME/.bashrc" ]; then
    SHELL_CONFIG="$USER_HOME/.bashrc"
elif [ -f "$USER_HOME/.zshrc" ]; then
    SHELL_CONFIG="$USER_HOME/.zshrc"
else
    echo "No supported shell config file found. Exiting."
    exit 1
fi

echo "Setting up alias for 'tweezer'..."
echo "alias tweezer='python $CURRENT_DIR/twz.py'" >> "$SHELL_CONFIG"

# Apply the changes to the current session
source "$SHELL_CONFIG"

# Ensure the Python files are executable
sudo chmod +x "$CURRENT_DIR/twz.py"
sudo chmod +x "$CURRENT_DIR/demo.py"
sudo chmod +x "$CURRENT_DIR/flag.py"

# Inform the user to reload their shell or restart terminal
echo "Setup complete! To use the tool, either restart the terminal or run 'source ~/.bashrc' or 'source ~/.zshrc'."
