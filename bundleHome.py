import os
import shutil

# Directory to search
root_dir = './Firmware/Firmware/src'
# Output file
build_dir = './Firmware/Firmware/build'
output_dir = './Firmware/Firmware/build/home'

print("creating directories")
if not os.path.exists(build_dir):
    os.mkdir(build_dir)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)



def bundle_sensors(output_filename):
    print('\nbundling sensors...')
    sensor_dir = os.path.join(root_dir, 'home', 'sensors')
    sensor_imports = ["import machine\n",
                      "import json\n",
                      "import sys\n",
                      "import dht\n",
                      "import utime\n"]

    sensor_files = ["Timer.py",
                    "Button.py",
                    "DHT22.py",
                    "DimmableLED.py",
                    "Fan.py",
                    "MotionSensor.py",
                    "StatusLED.py"]
    
    output_path = os.path.join(build_dir, 'home', output_filename)
    with open(output_path, 'w') as outfile:
            for i in sensor_imports:
                outfile.write(i)

            for file in sensor_files:
                filepath = os.path.join(sensor_dir, file)
                with open(filepath, 'r') as infile:
                    outfile.write(f'# File: {filepath}\n')
                    for line in infile.readlines():
                        is_import = line.startswith("import") or line.startswith('from')
                        if not is_import:
                            outfile.write(line)
                    outfile.write('\n\n')  # Separate files with some space
    print("finished")


def bundle_lib(output_filename):
    print("\nbundling lib...")
    lib_dir = os.path.join(root_dir, 'home', 'managers', 'lib')
    lib_imports = ["import usocket as _socket\n",
                   "import ustruct as struct\n",]
    lib_files = ["umqtt/simple.py",
                 "ftplib.py"]
    output_path = os.path.join(build_dir, 'home', output_filename)
    with open(output_path, 'w') as outfile:
            for i in lib_imports:
                outfile.write(i)

            for file in lib_files:
                filepath = os.path.join(lib_dir, file)
                with open(filepath, 'r') as infile:
                    outfile.write(f'# File: {filepath}\n')
                    for line in infile.readlines():
                        is_import = line.startswith("import") or line.startswith('from')
                        if not is_import:
                            outfile.write(line)
                    outfile.write('\n\n')  # Separate files with some space
    print("finished")


def bundle_managers(output_filename):
    print("\nbundling managers...")
    manager_dir = os.path.join(root_dir, 'home', 'managers')
    manager_files = [
    "CommandMessage.py",
    "ConfigManager.py",
    "MQTTManager.py",
    "SensorManager.py",
    "UpdateManager.py",
    "WiFiManager.py",
    ]
    manager_imports = [
    "import json\n",
    "import home\n",
    "import urequests\n",
    "import sys\n",
    "import utime\n",
    "import machine\n",
    "import ubinascii\n",
    "import os\n",
    "import uos\n",
    "import errno\n",
    "import network\n",
    "import home\n",
    "from .lib import MQTTClient, MQTTException, FTP\n",
    "from .sensors import HomeMotionSensor, HomeWeatherSensor, HomeLEDDimmer, HomeFan, HomeButton\n", 
]
    output_path = os.path.join(build_dir, 'home', output_filename)
    with open(output_path, 'w') as outfile:
            for i in manager_imports:
                outfile.write(i)

            for file in manager_files:
                filepath = os.path.join(manager_dir, file)
                with open(filepath, 'r') as infile:
                    outfile.write(f'# File: {filepath}\n')
                    for line in infile.readlines():
                        is_import = line.startswith("import") or line.startswith('from')
                        if not is_import:
                            outfile.write(line)
                    outfile.write('\n\n')  # Separate files with some space
    print('finished')


def copy_home():
    print('\ncopying additional files...')
    def copy_home_file():
        home = os.path.join(root_dir, 'home/Home.py')
        dest = os.path.join(build_dir, 'home', 'Home.py')
        shutil.copyfile(home, dest)
        
    def copy_init_file():
        home = os.path.join(root_dir, 'home/__init__.py')
        dest = os.path.join(build_dir, 'home', '__init__.py')
        shutil.copyfile(home, dest)

    def copy_main_file():
        main = os.path.join(root_dir, 'main.py')
        dest = os.path.join(build_dir, 'main.py')
        shutil.copyfile(main, dest)
    
    def copy_config_file():
        config = os.path.join(root_dir, 'config.json')
        dest = os.path.join(build_dir, 'config.json')
        shutil.copyfile(config, dest)

    copy_home_file()
    copy_init_file()
    copy_main_file()
    copy_config_file()
    print('finished')


# Run bundling
bundle_lib("lib.py")
bundle_managers("managers.py")
bundle_sensors("sensors.py")
copy_home()
