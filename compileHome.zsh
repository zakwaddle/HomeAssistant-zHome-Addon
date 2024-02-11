#!/bin/bash

# Source and destination directories
src_dir="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/Firmware/src/home"
dest_dir="/Users/zakwaddle/GitHub/HomeAssistant-zHome-Addon/Firmware/dist/home"

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
    mpy-cross "$file" -o "${dest_file%.py}.mpy"
done