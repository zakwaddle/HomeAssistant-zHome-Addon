#!/bin/bash

/usr/local/bin/python3 ./bundleHome.py  

./compileBuildFolder.zsh

/usr/local/bin/python3 ./Firmware/UpdateScripts/upload_firmware.py      