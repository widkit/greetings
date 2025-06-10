from datetime import datetime; import os, subprocess, requests, pytz, platform, yaml, sys

# Check if running as PyInstaller binary
def is_binary():
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# Get home directory and config paths
home_dir = os.path.expanduser("~")
config_dir = os.path.join(home_dir, ".config/greetings")
date_dir_file = os.path.join(config_dir, "date.txt")
config_file = os.path.join(config_dir, "greetings.yaml")

def createConfig():
    default_config = {
            'save_images': False,
            'flags': ["--color", "--color-bg", "-b"]
        }
    with open(config_file, 'w') as f:
        yaml.safe_dump(default_config, f, default_flow_style=False)

# Create config directory and files if they don't exist
if not os.path.exists(config_dir):
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(os.path.join(config_dir, "images"))
    open(date_dir_file, 'w').close()
    createConfig()

# Read configuration
try:
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
        save_images = config.get('save_images', False)
        flags = config.get('flags', ["--color", "--color-bg", "-b"])        
except (FileNotFoundError, yaml.YAMLError):
    print("No config file found. Using default settings.")
    save_images = False
    flags = ["--color", "--color-bg", "-b"]
    createConfig()

# Check if ascii-image-converter needs to be installed
try:
    subprocess.run(["ascii-image-converter", "--version"], check=True, capture_output=True)
except (subprocess.CalledProcessError, FileNotFoundError):
    print("Installing ascii-image-converter...")
    try:
        if is_binary():
            # When running as binary, run setup directly
            import setup
            setup.main()
        else:
            # When running as source, run setup.py as a script
            subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "setup.py")], check=True)
    except Exception as e:
        print(f"Failed to run setup: {e}")
        sys.exit(1)

# Assign today's date to a variable (in UTC, as Bing refreshes their wallpapers by UTC)
utc_now = datetime.now(pytz.utc)
utc_date = utc_now.date()
date_utc = str(utc_date).replace("-", "_")

# Set image path
if save_images:
    image_file = os.path.join(config_dir, "images", f"image_{date_utc}.jpg")
else:
    image_file = os.path.join(config_dir, "image.jpg")

# Check if date is equal to last used date of the script. If not, fetch the new image.
try: 
    with open(date_dir_file, "r") as f:
        last_date = f.read()
except FileNotFoundError:
    last_date = ""

if last_date != date_utc or not os.path.exists(image_file):
    if not save_images and os.path.isfile(image_file):
        os.remove(image_file)
    try:
        res = requests.get('https://bing.biturl.top/', timeout=10)
        res.raise_for_status()
        link = res.json().get("url")
        if not link:
            print("Error: No image URL found in response")
            sys.exit(1)
        daily_image = requests.get(link, timeout=10).content
        with open(image_file, 'wb') as handler:
            handler.write(daily_image)
        with open(date_dir_file, "w") as f:
            f.write(date_utc)
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
        sys.exit(1)

# Convert the image to colorful ASCII using ascii-image-converter and print it.
try:
    binary_name = r"C:\Program Files\TheZoraiz\ascii-image-converter\ascii-image-converter.exe" if platform.system().upper() == 'WINDOWS' else "ascii-image-converter"
    subprocess.run([binary_name, *flags, image_file], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running ascii-image-converter: {e}")
    sys.exit(1)
