import os, subprocess, platform, shutil, tarfile, zipfile, yaml

# Detect the operating system and architecture to select the correct binary for ascii-image-converter
system = platform.system().upper()
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
        useFile = True
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
    case 'DARWIN':
        match machine:
            case 'X86_64':
                releaseName = "ascii-image-converter_macOS_amd64_64bit.tar.gz"
            case 'ARM64':
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
if system != 'WINDOWS':
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
config_file = os.path.join(config_dir, "greetings.yaml")

if not os.path.exists(config_dir):
    print(f"Creating files at: {config_dir}")
    os.makedirs(config_dir)
    os.makedirs(os.path.join(config_dir, "images"))
    open(date_dir_file, 'w').close()
    # Create default config file in YAML format
    default_config = {
        'save_images': False,
    }
    with open(config_file, 'w') as f:
        yaml.safe_dump(default_config, f, default_flow_style=False)

print("Setup complete.")
