#!/bin/zsh

SOURCE_DIR="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/FlaskApp/"
DEST_DIR="root@homeassistant.local:~/addons/FlaskApp/"

# List of directories and files to exclude
EXCLUDE_PATTERNS=('.idea' '__pycache__' '.pyc' '*/__pycache__' 'venv' 'data' 'tests' 'sync.zsh' 'log_entries.db')

# Function to copy files excluding the specified patterns
copy_files_excluding() {
    for file in "$SOURCE_DIR"*; do
        skip=
        for pattern in "${EXCLUDE_PATTERNS[@]}"; do
            if [[ "$file" == *"$pattern"* ]]; then
                skip=1
                break
            fi
        done
        [[ -n $skip ]] || scp -r "$file" "$DEST_DIR"
    done
}

# Execute the copy function
copy_files_excluding