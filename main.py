from datetime import datetime
import os
import subprocess
import requests
import pytz

save_images = False
# Uncomment below to save the images
save_images = True


# Check if "ascii-image-converter" is installed.
dep_check = subprocess.call(['which', 'ascii-image-converter'], stdout=subprocess.DEVNULL)
if dep_check != 0:
    print('ascii-image-converter is not installed or not in $PATH.')
    exit()

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
if save_images == True:
    image_file = config_dir + f"/images/image_{date_utc}.jpg"
elif save_images == False:
    image_file = config_dir + "/image.jpg"



# Check if date is equal to last used date of the script. If not, fetch the new image.
f = open(date_dir_file, "r")
if f.read() != date_utc:
   f.close()
   if save_images != True:
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
os.system(f"ascii-image-converter -b --color --color-bg {image_file}")




