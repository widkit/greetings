import os, subprocess, platform, shutil, tarfile, zipfile, yaml, sys, requests, ctypes

def main():
    # Detect the operating system and architecture to select the correct binary for ascii-image-converter
    system = platform.system().upper()
    machine = platform.machine().upper()

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Get home directory and config paths
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config/greetings")

    if not os.path.exists(config_dir):
        print(f"Creating files at: {config_dir}")
        os.makedirs(config_dir, exist_ok=True)
        os.makedirs(os.path.join(config_dir, "images"))
        config_file = os.path.join(config_dir, "greetings.yaml")
        date_dir_file = os.path.join(config_dir, "date.txt")
        open(date_dir_file, 'w').close()
        default_config = {
                'save_images': False,
            }
        with open(config_file, 'w') as f:
            yaml.safe_dump(default_config, f, default_flow_style=False)

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
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("Please run the program as administrator for the setup.")
                sys.exit(1)
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

    # Construct the download URL
    downloadURL = f"https://github.com/TheZoraiz/ascii-image-converter/releases/download/{ascii_image_converter_latestRelease}/{releaseName}"

    # Download the file
    try:
        print(f"Downloading {releaseName} from release {ascii_image_converter_latestRelease}...")
        response = requests.get(downloadURL, timeout=30)
        response.raise_for_status()
        outputFile = os.path.join(config_dir, releaseName)
        with open(outputFile, 'wb') as f:
            f.write(response.content)
        print(f"{outputFile} downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

    # Extract the downloaded file
    extract_dir = os.path.join(config_dir, "ascii-image-converter")
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
            unixOS = 'linux'
        elif system == 'DARWIN':
            unixOS = 'macos'
        binary_path = os.path.join(extract_dir, releaseName.replace('.tar.gz', ''), 'ascii-image-converter')
        subprocess.run(["chmod", "+x", binary_path], check=True)
        try:
            print("Moving the binaries to /usr/local/bin (you may be prompted for your password)...")
            subprocess.run(["sudo", "mv", binary_path, "/usr/local/bin/ascii-image-converter"], check=True)
            subprocess.run(["sudo", "cp", f"greetings-{unixOS}", "/usr/local/bin/greetings"], check=True)
        except Exception as e:
            print(f"Failed to move binaries: {e}")
            sys.exit(1)
    else:
        os.makedirs("C:\\Program Files\\TheZoraiz\\ascii-image-converter", exist_ok=True)
        os.makedirs("C:\\Program Files\\widkit\\greetings", exist_ok=True)
        binary_path = os.path.join(extract_dir, releaseName.replace('.zip', ''), 'ascii-image-converter.exe')
        shutil.move(binary_path, "C:\\Program Files\\TheZoraiz\\ascii-image-converter\\ascii-image-converter.exe")
        shutil.copy("greetings-windows.exe", "C:\\Program Files\\widkit\\greetings\\greetings.exe")


    # Cleanup
    print("Cleaning up...")
    try:
        shutil.rmtree(extract_dir)
        os.remove(outputFile)
    except Exception as e:
        print(f"Error deleting the files: {e}")

    print("Setup complete.")

if __name__ == "__main__":
    main()