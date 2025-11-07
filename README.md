# greetings

<div align="center">

![greetings](https://github.com/user-attachments/assets/507ac856-4298-4fb6-ae2c-14ece783654b)

![Python Version](https://img.shields.io/badge/python-3.10+-3776AB)
![License](https://img.shields.io/badge/license-GPLv3-4CAF50)
![Release](https://img.shields.io/github/v/release/widkit/greetings?color=F39C12)
![Issues](https://img.shields.io/github/issues/widkit/greetings?color=E74C3C)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-8E44AD)
![ASCII Art](https://img.shields.io/badge/ascii-art-FF69B4)


</div>

A simple Python script that fetches a picture from Bing or Picsum daily, and converts it to colorful ASCII art using [ascii-image-converter](https://github.com/widkit/ascii-image-converter).

## Quick Links

- [Installation](#installation)
- [Using the script](#using-the-script)
- [Using as a color script](#using-as-a-color-script)
- [Tips](#tips)
- [Customization](#customization)
  - [Available Flags](#available-flags)
- [Full Manpage](#full-manpage)

## Installation

### Option 1: Pre-built Executables (Recommended)
Download the latest release for your platform from [Releases page](https://github.com/widkit/greetings/releases):
- Windows: `greetings-windows.exe`
- macOS: `greetings-macos`
- Linux: `greetings-linux`

After downloading:

1. Make the file executable (Linux/macOS):
   ```bash
   chmod +x greetings-linux  # or greetings-macos
   ```
2. Run the executable:

   ```bash
   # Windows
   .\greetings-windows.exe
   ```
> [!NOTE]  
> On Windows, the installer must be executed with administrator privileges. These privileges are not required for the application to run after installation.
   ```bash
   # Linux/macOS
   ./greetings-linux  # or ./greetings-macos
   ```
> [!NOTE]  
> The binaries will be moved to ~/.local/bin. Make sure you add it to your PATH if not already added.

### Option 2: From Source
Requirements:
* Python 3.10 or higher (for match/case support)
* [requests](https://pypi.org/project/requests/)
* [pytz](https://github.com/stub42/pytz)

The program will automatically download and install the required [ascii-image-converter](https://github.com/widkit/ascii-image-converter) binary for your system on first run.

Clone the repository:
```bash
git clone https://github.com/widkit/greetings
```
cd into `greetings`:

```bash
cd greetings
```
Install dependencies via poetry:

```bash
poetry install
```

## Using the script
```bash
python3 src/greetings/main.py
```

### Building the script
```bash
pyinstaller --onefile src/greetings/main.py
```

## Using as a color script (runs at shell start-up)
### Windows
Create and edit a PowerShell profile:
```
notepad $PROFILE
```
Add the following line at the top:
```
# If using pre-built executable:
& "PATH-TO-EXECUTABLE/greetings-windows.exe"

# If using Python script:
python "PATH-TO-SCRIPT/src/main.py"
```
Replace the path with the absolute path to the executable or script.

### Unix (Mac, Linux)
Add line to your shell profile (~/.bashrc, ~/.zshrc, etc.):
```bash
# If using pre-built executable:
greetings

# If using Python script:
python "/path/to/src/main.py"
```

## Tips

- You can save the daily images by setting `save_images = True` in ~/.config/greetings/greetings.yaml
- Images are cached in ~/.config/greetings/ to avoid unnecessary downloads.

## Customization

The program can be customized through the configuration file located at `~/.config/greetings/greetings.yaml`. Here's an example configuration:

```yaml
save_images: false
flags:
  - -C
  - --color-bg
  - -b
  # To enable additional flags, uncomment and move them above this line
  # - -n
  # - -x
  # - -d
  # - 60,30
```

### Available Flags

#### Basic Flags
- `-C`: Display ASCII art with original colors
- `--color-bg`: Use color on character background instead of foreground
- `-b`: Use braille characters instead of ASCII
- `-g`: Display grayscale ASCII art
- `-c`: Use more ASCII characters for higher quality
- `-f`: Use largest dimensions that fill the terminal width
- `-n`: Display ASCII art in negative colors
- `-x`: Flip ASCII art horizontally
- `-y`: Flip ASCII art vertically

#### Flags with Parameters
These flags require two separate lines in the configuration:
```
- -d
- 60,30
```
- `-d`: Set width and height for ASCII art (e.g., 60,30)
- `-W`: Set width for ASCII art (height adjusts automatically)
- `-H`: Set height for ASCII art (width adjusts automatically)
- `-m`: Custom ASCII characters (ordered from darkest to lightest)

### Notes
- The configuration file is created automatically on first run
- Changes to the configuration take effect immediately
- Some flags may not work well together (e.g., `-C` overrides `-g`)
- Terminal must support the selected output options (e.g., colors, braille)

## Full Manpage

<details>
<summary>Click to expand full ascii-image-converter manual</summary>

```
ascii-image-converter [image paths/urls or piped stdin] [flags]

Flags:
  -C, --color             Display ascii art with original colors
                          If 24-bit colors aren't supported, uses 8-bit
                          (Inverts with --negative flag)
                          (Overrides --grayscale and --font-color flags)
                          
      --color-bg          If some color flag is passed, use that color
                          on character background instead of foreground
                          (Inverts with --negative flag)
                          (Only applicable for terminal display)
                          
  -d, --dimensions ints   Set width and height for ascii art in CHARACTER length
                          e.g. -d 60,30 (defaults to terminal height)
                          (Overrides --width and --height flags)
                          
  -W, --width int         Set width for ascii art in CHARACTER length
                          Height is kept to aspect ratio
                          e.g. -W 60
                          
  -H, --height int        Set height for ascii art in CHARACTER length
                          Width is kept to aspect ratio
                          e.g. -H 60
                          
  -m, --map string        Give custom ascii characters to map against
                          Ordered from darkest to lightest
                          e.g. -m " .-+#@" (Quotation marks excluded from map)
                          (Overrides --complex flag)
                          
  -b, --braille           Use braille characters instead of ascii
                          Terminal must support braille patterns properly
                          (Overrides --complex and --map flags)
                          
      --threshold int     Threshold for braille art
                          Value between 0-255 is accepted
                          e.g. --threshold 170
                          (Defaults to 128)
                          
      --dither            Apply dithering on image for braille
                          art conversion
                          (Only applicable with --braille flag)
                          (Negates --threshold flag)
                          
  -g, --grayscale         Display grayscale ascii art
                          (Inverts with --negative flag)
                          (Overrides --font-color flag)
                          
  -c, --complex           Display ascii characters in a larger range
                          May result in higher quality
                          
  -f, --full              Use largest dimensions for ascii art
                          that fill the terminal width
                          (Overrides --dimensions, --width and --height flags)
                          
  -n, --negative          Display ascii art in negative colors
                          
  -x, --flipX             Flip ascii art horizontally
                          
  -y, --flipY             Flip ascii art vertically
                          
  -s, --save-img string   Save ascii art as a .png file
                          Format: <image-name>-ascii-art.png
                          Image will be saved in passed path
                          (pass . for current directory)
                          
      --save-txt string   Save ascii art as a .txt file
                          Format: <image-name>-ascii-art.txt
                          File will be saved in passed path
                          (pass . for current directory)
                          
      --save-gif string   If input is a gif, save it as a .gif file
                          Format: <gif-name>-ascii-art.gif
                          Gif will be saved in passed path
                          (pass . for current directory)
                          
      --save-bg ints      Set background color for --save-img
                          and --save-gif flags
                          Pass an RGBA value
                          e.g. --save-bg 255,255,255,100
                          (Defaults to 0,0,0,100)
                          
      --font string       Set font for --save-img and --save-gif flags
                          Pass file path to font .ttf file
                          e.g. --font ./RobotoMono-Regular.ttf
                          (Defaults to Hack-Regular for ascii and
                           DejaVuSans-Oblique for braille)
                          
      --font-color ints   Set font color for terminal as well as
                          --save-img and --save-gif flags
                          Pass an RGB value
                          e.g. --font-color 0,0,0
                          (Defaults to 255,255,255)
                          
      --only-save         Don't print ascii art on terminal
                          if some saving flag is passed
                          
      --formats           Display supported input formats
                          
  -h, --help              Help for ascii-image-converter
                          
  -v, --version           Version for ascii-image-converter
```
</details>


