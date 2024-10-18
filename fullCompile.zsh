#!/bin/bash

cd ./ReactApp
npm run build
cd ..

cd ./FlaskApp
./sync.zsh

cd ..
./compileHome.zsh

/usr/local/bin/python3 ./Firmware/UpdateScripts/upload_firmware.py      