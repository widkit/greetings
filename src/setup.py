import os, subprocess, platform, shutil, tarfile, zipfile, yaml, sys, requests

def main():
    # Detect the operating system and architecture to select the correct binary for ascii-image-converter
    system = platform.system().upper()
    machine = platform.machine().upper()

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Fetch the latest release of ascii-image-converter from GitHub using requests
    try:
        response = requests.get('https://api.github.com/repos/TheZoraiz/ascii-image-converter/releases/latest', timeout=10)
        response.raise_for_status()
        ascii_image_converter_latestRelease = response.json()['tag_name']
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching the latest release: {e}")
        sys.exit(1)

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
                    sys.exit(1)
        case 'DARWIN':
            match machine:
                case 'X86_64':
                    releaseName = "ascii-image-converter_macOS_amd64_64bit.tar.gz"
                case 'ARM64':
                    releaseName = "ascii-image-converter_macOS_arm64_64bit.tar.gz"
                case _:
                    print(f"Unknown macOS architecture '{machine}'.")
                    sys.exit(1)
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
                    sys.exit(1)
        case _:
            print(f"Unsupported operating system '{system}'.")
            sys.exit(1)

    # Create a temporary directory for downloads
    temp_dir = os.path.join(os.path.expanduser("~"), ".config", "greetings", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    os.chdir(temp_dir)

    # Construct the download URL
    downloadURL = f"https://github.com/TheZoraiz/ascii-image-converter/releases/download/{ascii_image_converter_latestRelease}/{releaseName}"

    # Define the output file path
    outputFile = os.path.join(temp_dir, releaseName)

    # Download the file with curl
    try:
        print(f"Downloading {releaseName} from release {ascii_image_converter_latestRelease}...")
        response = requests.get(downloadURL, timeout=30)
        response.raise_for_status()
        with open(outputFile, 'wb') as f:
            f.write(response.content)
        print(f"{outputFile} downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

    # Extract the downloaded file
    extract_dir = os.path.join(temp_dir, "ascii-image-converter")
    if releaseName.endswith(".zip"):
        try:
            with zipfile.ZipFile(outputFile, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print("File extracted successfully.")
        except Exception as e:
            print(f"Error extracting file: {e}")
            sys.exit(1)

    elif releaseName.endswith(".tar.gz"):
        try:
            with tarfile.open(outputFile, "r:gz") as tar_ref:
                tar_ref.extractall(extract_dir)
            print("File extracted successfully.")
        except Exception as e:
            print(f"Error extracting file: {e}")
            sys.exit(1)
    else:
        print("Error extracting file: Unsupported file format.")
        sys.exit(1)

    # Check if the operating system is not Windows
    if system != 'WINDOWS':
        if system == 'LINUX': # Assign the platform to match the binary name
            platform = 'linux'
        elif system == 'DARWIN':
            platform = 'macos'
        binary_path = os.path.join(extract_dir, releaseName.replace('.tar.gz', ''), 'ascii-image-converter')
        subprocess.run(["chmod", "+x", binary_path], check=True)
        try:
            print("Moving the binaries to /usr/local/bin (you may be prompted for your password)...")
            subprocess.run(["sudo", "mv", binary_path, "/usr/local/bin/ascii-image-converter"], check=True)
            subprocess.run(["sudo", "cp", f"./greetings-{platform}", "/usr/local/bin/greetings"], check=True)
        except Exception as e:
            print(f"Failed to move binaries: {e}")
            sys.exit(1)

    # Cleanup
    print("Cleaning up...")
    try:
        shutil.rmtree(temp_dir)
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

if __name__ == "__main__":
    main()