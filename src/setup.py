import os, subprocess, platform, shutil, tarfile, zipfile, sys, requests, ctypes

def create_default_config():
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config/greetings")
    config_file = os.path.join(config_dir, "greetings.yaml")
    config_text = '''# greetings configuration file
save_images: false
flags:
- -C
- --color-bg
- -b
#- -d
#- 60,30
#- -W
#- 60
#- -H
#- 60
#- -m
#- .-+#@
#- -g
#- -c
#- -f
#- -n
#- -x
#- -y
# Since PyYAML parser is sensitive to inline and in between comments, flags must be moved just after the active flags.
# Flag descriptions:
# -C          Display ascii art with original colors
# --color-bg  Use color on character background
# -b          Use braille characters
# -g          Display grayscale ascii art
# -c          Use more ascii chars
# -f          Use largest dimensions
# -n          Negative colors
# -x          Flip horizontally
# -y          Flip vertically
#
# The following flags must be used in two separate lines:
# Example:
# -d
# 60,30
#
# -d 60,30    Set width and height for ascii art
# -W 60       Set width for ascii art
# -H 60       Set height for ascii art
# -m .-+#@    Custom ascii characters
'''
    with open(config_file, 'w') as f:
        f.write(config_text)

def main():
    # Detect the operating system and architecture to select the correct binary for ascii-image-converter.
    system = platform.system().upper()
    machine = platform.machine().upper()

    # Get the directory where the script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Get home directory and config paths.
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config/greetings")

    # Install target
    targetDir = os.path.join(home_dir, ".local/bin/")
    asciiTarget = os.path.join(targetDir, "ascii-image-converter")
    greetingsTarget = os.path.join(targetDir, "greetings")

    config_file = os.path.join(config_dir, "greetings.yaml") # Define files.
    date_dir_file = os.path.join(config_dir, "date.txt")
    if not os.path.exists(config_dir):
        print(f"Creating files at: {config_dir}")
        os.makedirs(config_dir, exist_ok=True) # Create config directories.
        os.makedirs(os.path.join(config_dir, "images"))
        open(date_dir_file, 'w').close() # Create date file.
        create_default_config()
    elif not os.path.exists(config_file):
        create_default_config()

    # Fetch the latest release of ascii-image-converter from GitHub using requests.
    try:
        response = requests.get('https://api.github.com/repos/widkit/ascii-image-converter/releases/latest', timeout=10) # Get latest release tag.
        response.raise_for_status()
        ascii_image_converter_latestRelease = response.json()['tag_name']
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching the latest release: {e}")
        sys.exit(1)

    # Detect the architecture and the OS, set the release name.
    match system:
        case 'WINDOWS':
            if not ctypes.windll.shell32.IsUserAnAdmin(): # Check if ran as administrator for further in setup.
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

    # Construct the download URL.
    downloadURL = f"https://github.com/widkit/ascii-image-converter/releases/download/{ascii_image_converter_latestRelease}/{releaseName}"

    # Download the file.
    try:
        print(f"Downloading {releaseName} from release {ascii_image_converter_latestRelease}...")
        response = requests.get(downloadURL, timeout=30)
        response.raise_for_status()
        outputFile = os.path.join(config_dir, releaseName)
        with open(outputFile, 'wb') as f: # Write to disk.
            f.write(response.content)
        print(f"{outputFile} downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

    # Extract the downloaded file.
    extract_dir = os.path.join(config_dir, "ascii-image-converter")
    binary_path = None # Initialize binary_path to None
    
    if releaseName.endswith(".zip"): # Extracts the correct file with correct library.
        try:
            with zipfile.ZipFile(outputFile, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print("File extracted successfully.")
            
            # Search for the executable in the extracted directory
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    if file == ('ascii-image-converter.exe' if system == 'WINDOWS' else 'ascii-image-converter'):
                        binary_path = os.path.join(root, file)
                        break
                if binary_path:
                    break # Found it, stop searching

        except Exception as e:
            print(f"Error extracting file: {e}")
            sys.exit(1)

    elif releaseName.endswith(".tar.gz"):
        try:
            # Add filter='data' to prevent the DeprecationWarning in Python 3.14+
            with tarfile.open(outputFile, "r:gz") as tar_ref:
                tar_ref.extractall(extract_dir, filter='data') 
            print("File extracted successfully.")
            
            # Search for the executable in the extracted directory
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    if file == 'ascii-image-converter':
                        binary_path = os.path.join(root, file)
                        break
                if binary_path:
                    break # Found it, stop searching

        except Exception as e:
            print(f"Error extracting file: {e}")
            sys.exit(1)
    else:
        print("Error extracting file: Unsupported file format.")
        sys.exit(1)

    # Check if the operating system is not Windows.
    if system != 'WINDOWS':
        if system == 'LINUX': # Assign the platform to match the binary name.
            unixOS = 'linux'
        elif system == 'DARWIN':
            unixOS = 'macos'
        
        # Verify binary_path was found during extraction
        if not binary_path or not os.path.exists(binary_path):
            print(f"Error: Expected binary 'ascii-image-converter' not found after extraction in '{extract_dir}'.")
            sys.exit(1)

        try:
            subprocess.run(["chmod", "+x", binary_path], check=True) # Set as executable.
        except subprocess.CalledProcessError as e:
            print(f"Failed to set executable permissions on '{binary_path}': {e}")
            sys.exit(1)

        greetingsSrc = os.path.join(script_dir, f"greetings-{unixOS}")
        try:
            print("Moving the binaries to ~/.local/bin...")
            os.makedirs(targetDir, exist_ok=True)
            shutil.move(binary_path, asciiTarget)
            shutil.copy2(greetingsSrc, greetingsTarget)
        except Exception as e:
                print(f"Failed to move binaries: {e}")
                sys.exit(1)
        path_env = os.environ.get('PATH', '')
        if targetDir not in path_env.split(os.pathsep):
            print("Warn: ~/.local/bin not in PATH! Please add it to your PATH for the program to work correctly.")
    else: # Windows
        os.makedirs("C:\\Program Files\\widkit\\ascii-image-converter", exist_ok=True) # Make directories for ascii-image-converter and greetings.
        os.makedirs("C:\\Program Files\\widkit\\greetings", exist_ok=True)
        
        # Verify binary_path was found during extraction
        if not binary_path or not os.path.exists(binary_path):
            print(f"Error: Expected binary 'ascii-image-converter.exe' not found after extraction in '{extract_dir}'.")
            sys.exit(1)

        shutil.move(binary_path, "C:\\Program Files\\widkit\\ascii-image-converter\\ascii-image-converter.exe") # Moves the file.
        shutil.copy("greetings-windows.exe", "C:\\Program Files\\widkit\\greetings\\greetings.exe") # Copies itself into Program Files.

    # Clean up.
    print("Cleaning up...")
    try:
        shutil.rmtree(extract_dir) # Delete downloaded files.
        os.remove(outputFile)
    except Exception as e:
        print(f"Error deleting the files: {e}")

    print("Setup complete.")

if __name__ == "__main__": # Return to main.py
    main()
