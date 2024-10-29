#!/bin/bash

# build React app into Flask static folder
build_react_app() {
    echo ""
    echo ""
    echo "----------------------------------------------------------"
    echo "                   Building React App"
    echo "----------------------------------------------------------"
    cd ./ReactApp
    npm run build
    cd ..
}


# upload Flask app to Home Assistant
upload_flask_app() {
    echo ""
    echo ""
    echo "----------------------------------------------------------"
    echo "          Uploading Flask App to Home Assistant"
    echo "----------------------------------------------------------"
    FLASK_DIR="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/FlaskApp/"
    HA_DIR="root@homeassistant.local:~/addons/FlaskApp/"

    # List of directories and files to exclude
    EXCLUDE_PATTERNS=('.idea' '__pycache__' '*.pyc' '*/__pycache__' 'venv' 'data' 'tests' 'sync.zsh' 'log_entries.db' '.DS_Store')

    for file in "$FLASK_DIR"*; do
            skip=
            for pattern in "${EXCLUDE_PATTERNS[@]}"; do
                if [[ "$file" == *"$pattern"* ]]; then
                    skip=1
                    break
                fi
            done
            [[ -n $skip ]] || scp -r "$file" "$HA_DIR"
        done

    # copy the stuff that the function is missing

    SOURCE_FILE="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/FlaskApp/database/__init__.py"
    DEST_DIR2="root@homeassistant.local:~/addons/FlaskApp/database/"
    scp -r "$SOURCE_FILE" "$DEST_DIR2"

    SOURCE_FILE3="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/FlaskApp/.flaskenv"
    DEST_DIR3="root@homeassistant.local:~/addons/FlaskApp/"
    scp -r "$SOURCE_FILE3" "$DEST_DIR3"

}


# bundle micropython code into build dir
bundle_micropython() {
    echo ""
    echo ""
    echo "----------------------------------------------------------"
    echo "                  Bundling Home Package"
    echo "----------------------------------------------------------"
    /usr/local/bin/python3 ./bundleHome.py
}


# compile build dir into .mpy files
compile_mpy_files() {
    echo ""
    echo ""
    echo "----------------------------------------------------------"
    echo "                  Compiling .mpy files"
    echo "----------------------------------------------------------"
    # Source and destination directories
    src_dir="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/Firmware/Firmware/build/home"
    dest_dir="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/Firmware/Firmware/build-dist/home"

    # Check if destination directory exists, create if not
    if [ ! -d "$dest_dir" ]; then
    mkdir -p "$dest_dir"
    fi

    # Compile all .py files to .mpy and move to destination directory
    find "$src_dir" -name '*.py' | while read -r file
    do
        dest_file="${dest_dir}${file#$src_dir}"
        dest_path=$(dirname "$dest_file")

        mkdir -p "$dest_path"
        echo "compiling $file"
        mpy-cross "$file" -o "${dest_file%.py}.mpy"
    done
    
    echo "copying additional files"
    cp "${src_dir}/../main.py" "${dest_dir}/../main.py"
    cp "${src_dir}/../config.json" "${dest_dir}/../config.json"
}

# upload compiled .mpy files to home assistant ftp server
upload_home_to_ftp_server() {
    echo ""
    echo ""
    echo "----------------------------------------------------------"
    echo "    Uploading .mpy files to Home Assistant FTP server"
    echo "----------------------------------------------------------"
    /usr/local/bin/python3 ./Firmware/UpdateScripts/upload_firmware.py      
}


build_react_app
upload_flask_app
bundle_micropython
compile_mpy_files
upload_home_to_ftp_server