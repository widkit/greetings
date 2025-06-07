from datetime import datetime
import os
import subprocess
import requests
import pytz
import platform
import shutil
import tarfile
import zipfile

# Uncomment below to save the images
save_images = True

# Detect the operating system and architecture to select the correct binary for ascii-image-converter
system = platform.system().upper() # Uppercase to foolproof the string check
machine = platform.machine().upper()

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Fetch the latest release of ascii-image-converter from GitHub
curlCommand = "curl -s https://api.github.com/repos/TheZoraiz/ascii-image-converter/releases/latest | grep -oP '\"tag_name\": \"\\K[^\"]+'" 
try:
    ascii_image_converter_latestRelease = subprocess.check_output(curlCommand, shell=True).decode('utf-8').strip()
except subprocess.CalledProcessError as e:
    print(f"Error fetching the latest release: {e}")
    exit(1)

# Default
useFile = False

# Detect the architecture and the OS, set the release name 
match system:
    case 'WINDOWS':
        useFile = True # For Windows, we use the bin file cz Windows PATH is fucking stupid.
        match machine:
            case 'AMD64' | 'X86_64':
                releaseName = "ascii-image-converter_Windows_amd64_64bit.zip"
            case 'ARM64':
                releaseName = "ascii-image-converter_Windows_arm64_64bit.zip"
            case 'ARMV6' | 'ARMV6l':
                releaseName = "ascii-image-converter_Windows_armv6_32bit.zip"
            case 'I386' | 'I686':
                releaseName = "ascii-image-converter_Windows_i386_32bit.zip"
            case _:
                print(f"Unknown Windows architecture '{machine}'.")
                exit(1)

    case 'DARWIN': # macOS
        match machine:
            case 'X86_64': # Intel
                releaseName = "ascii-image-converter_macOS_amd64_64bit.tar.gz"
            case 'ARM64': # Apple Silicon
                releaseName = "ascii-image-converter_macOS_arm64_64bit.tar.gz"
            case _: 
                print(f"Unknown macOS architecture '{machine}'.")
                exit(1)

    case 'LINUX':
        match machine:
            case 'X86_64': 
                releaseName = "ascii-image-converter_Linux_amd64_64bit.tar.gz"
            case 'AARCH64' | 'ARM64': 
                releaseName = "ascii-image-converter_Linux_arm64_64bit.tar.gz"
            case 'ARMV6L' | 'ARMV6':
                releaseName = "ascii-image-converter_Linux_armv6_32bit.tar.gz"
            case 'I386' | 'I686':
                releaseName = "ascii-image-converter_Linux_i386_32bit.tar.gz"
            case _: 
                print(f"Unknown Linux architecture '{machine}'.")
                exit(1)

    case _:
        print(f"Unsupported operating system '{system}'.")
        exit(1)

# Construct the download URL
downloadURL = f"https://github.com/TheZoraiz/ascii-image-converter/releases/download/{ascii_image_converter_latestRelease}/{releaseName}"

# Define the output file path
outputFile = releaseName

# Download the file with curl
try:
    print(f"Downloading {releaseName} from release {ascii_image_converter_latestRelease}...")
    subprocess.check_call(["curl", "-L", "-o", outputFile, downloadURL])
    print(f"{outputFile} downloaded successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error downloading file: {e}")
    exit(1)

# Extract the downloaded file
if releaseName.endswith(".zip"):
    try:
        with zipfile.ZipFile(outputFile, 'r') as zip_ref:
            zip_ref.extractall("ascii-image-converter")
        print("File extracted successfully.")
    except Exception as e:
        print(f"Error extracting file: {e}")
        exit(1)

elif releaseName.endswith(".tar.gz"):
    try:
        with tarfile.open(outputFile, "r:gz") as tar_ref:
            tar_ref.extractall("ascii-image-converter")
        print("File extracted successfully.")
    except Exception as e:
        print(f"Error extracting file: {e}")
        exit(1)
else:
    print("Error extracting file: Unsupported file format.")
    exit(1)

# Set the binary as executable
if system != 'WINDOWS': # For Windows it's already executable 
    subprocess.run(["chmod", "+x", "ascii-image-converter/ascii-image-converter"], check=True)

# Move the binary to /usr/local/bin (Linux/macOS)
try:
    print("Moving the binary to /usr/local/bin (you may be prompted for your password)...")
    subprocess.run(["sudo", "mv", "ascii-image-converter/ascii-image-converter", "/usr/local/bin/ascii-image-converter"], check=True)
except subprocess.CalledProcessError:
    print("Failed to move binary. Please manually run: \"sudo mv ascii-image-converter/ascii-image-converter /usr/local/bin/\"")
    exit(1)

# Cleanup
print("Cleaning up...")
try:
    shutil.rmtree("ascii-image-converter")
    os.remove(outputFile)
except Exception as e:
    print(f"Error deleting the files: {e}")

# Get the home directory
home_dir = os.path.expanduser("~")

# Check if the directory exists, if not create it and output the directory of the files to the user.
config_dir = os.path.join(home_dir, ".config/greetings")
date_dir_file = os.path.join(config_dir, "date.txt")

if not os.path.exists(config_dir):
    print(f"Creating files at: {config_dir}")
    os.makedirs(config_dir)
    os.makedirs(os.path.join(config_dir, "images"))
    open(date_dir_file, 'w').close()

# Assign today's date to a variable (in UTC, as Bing refreshes their wallpapers by UTC)
utc_now = datetime.now(pytz.utc)
utc_date = utc_now.date()
date_utc = str(utc_date).replace("-", "_")

# Check if the save_images is enabled.
if save_images:
    image_file = os.path.join(config_dir, "images", f"image_{date_utc}.jpg")
elif not save_images:
    image_file = os.path.join(config_dir, "image.jpg")


# Check if date is equal to last used date of the script. If not, fetch the new image.
try: 
    with open(date_dir_file, "r") as f:
        last_date = f.read()
except FileNotFoundError:
    last_date = ""
if last_date != date_utc:
   if not save_images:
        # noinspection PyUnboundLocalVariable
        if os.path.isfile(image_file):
            os.remove(image_file)
   try:
        res = requests.get('https://bing.biturl.top/', timeout=10)
        res.raise_for_status()  # Raise an error for bad status codes
        link = res.json().get("url")
        if not link:
            print("Error: No image URL found in response")
            exit(1)
        daily_image = requests.get(link, timeout=10).content
        with open(image_file, 'wb') as handler:
            handler.write(daily_image)
        with open(date_dir_file, "w") as f:
            f.write(date_utc)
   except requests.RequestException as e:
       print(f"Error fetching image: {e}")
       exit(1)

# Convert the image to colorful ASCII using ascii-image-converter and print it.
if useFile:
    subprocess.run(["./ascii-image-converter/ascii-image-converter.exe", "-b", "--color", "--color-bg", image_file], check=True)
else:
    subprocess.run(["ascii-image-converter", "-b", "--color", "--color-bg", image_file], check=True)
