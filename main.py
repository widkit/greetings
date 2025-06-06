from datetime import datetime
import os
import subprocess
import requests
import pytz
import platform

# Uncomment below to save the images
save_images = True

# Detect the operating system and architecture to select the correct binary for ascii-image-converter
system = platform.system()
machine = platform.machine()

match system:
    case 'Windows':
        match machine:
            case 'AMD64' | 'x86_64':
                ascii_image_converter_bin = "./bin/windows/amd64/ascii-image-converter.exe"
            case 'ARM64':
                ascii_image_converter_bin = "./bin/windows/arm64/ascii-image-converter.exe"
            case _: 
                print(f"Unknown Windows architecture '{machine}'.")
                exit(1)

    case 'Darwin': # macOS
        match machine:
            case 'x86_64': # Intel 
                ascii_image_converter_bin = "./bin/macos/amd64/ascii-image-converter"
            case 'arm64': # Apple Silicon
                ascii_image_converter_bin = "./bin/macos/arm64/ascii-image-converter"
            case _: 
                print(f"Unknown macOS architecture '{machine}'.")
                exit(1)

    case 'Linux':
        match machine:
            case 'x86_64': 
                ascii_image_converter_bin = "./bin/linux/amd64/ascii-image-converter"
            case 'aarch64' | 'arm64': 
                ascii_image_converter_bin = "./bin/linux/arm64/ascii-image-converter"
            case _: 
                print(f"Unknown Linux architecture '{machine}'.")
                exit(1)

    case _:
        print(f"Unsupported operating system '{system}'.")
        exit(1)

# Get the home directory
home_dir = os.path.expanduser("~")

# Check if the directory exists, if not create it and output the directory of the files to the user.
config_dir = os.path.join(home_dir, ".config/greetings")
date_dir_file = config_dir + "/date.txt"

if not os.path.exists(config_dir):
    print(f"Creating files at: {config_dir}")
    os.makedirs(config_dir)
    os.makedirs(config_dir + "/images")
    open(date_dir_file, 'w').close()

# Assign today's date to a variable (in UTC, bing refreshes their wallpapers by UTC)
utc_now = datetime.now(pytz.utc)
utc_date = utc_now.date()
date_utc = str(utc_date).replace("-", "_")

# Check if the save_images is enabled.
if save_images:
    image_file = config_dir + f"/images/image_{date_utc}.jpg"
elif not save_images:
    image_file = config_dir + "/image.jpg"

# Check if date is equal to last used date of the script. If not, fetch the new image.
f = open(date_dir_file, "r")
if f.read() != date_utc:
   f.close()
   if not save_images:
       # noinspection PyUnboundLocalVariable
       if os.path.isfile(image_file):
           os.remove(image_file)
   res = requests.get('https://bing.biturl.top/')
   link = res.json().get("url")
   daily_image = requests.get(link).content
   with open(image_file, 'wb') as handler:
       handler.write(daily_image)
   f = open(date_dir_file, "w")
   f.write(date_utc)
   f.close()

# Convert the image to colorful ASCII using ascii-image-converter and print it.
os.system(f"{ascii_image_converter_bin} -b --color --color-bg {image_file}")




