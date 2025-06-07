# greetings

![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/v/release/widkit/greetings)
![Issues](https://img.shields.io/github/issues/widkit/greetings)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)
![ASCII Art](https://img.shields.io/badge/ascii-art-FF69B4)

A Python program that works on Mac, Linux and Windows which fetches the daily Bing wallpaper and converts it into colorful ASCII art. It may be used with shells as a color script, as seen in DistroTube's Youtube channel.

![greetings](https://github.com/user-attachments/assets/507ac856-4298-4fb6-ae2c-14ece783654b)

## Installation

### Option 1: Pre-built Executables (Recommended)
Download the latest release for your platform from [Releases page](https://github.com/widkit/greetings/releases):
- Windows: `greetings-windows.exe`
- macOS: `greetings-macos`
- Linux: `greetings-linux`

After downloading:

1. Install dependencies via pip:
   ```bash
   pip install -r requirements.txt
   ```
2. Make the file executable (Linux/macOS):
   ```bash
   chmod +x greetings-linux  # or greetings-macos
   ```
3. Run the executable:
   ```bash
   # Windows
   greetings-windows.exe
   ```
   ```bash
   # Linux/macOS
   ./greetings-linux  # or ./greetings-macos
   ```

4. (Optional) For system-wide installation on Linux/macOS:
   ```bash
   # Move to /usr/local/bin for system-wide access
   sudo mv greetings-linux /usr/local/bin/greetings  # or greetings-macos
   
   # Now you can run it from anywhere
   greetings
   ```

   For Windows, you can:
   1. Create a directory in Program Files: `C:\Program Files\greetings`
   2. Move the executable there
   3. Add the directory to your PATH environment variable

### Option 2: From Source
Requirements:
* Python 3.10 or higher (for match/case support)
* [requests](https://pypi.org/project/requests/)
* [pytz](https://github.com/stub42/pytz)

The program will automatically download and install the required [ascii-image-converter](https://github.com/TheZoraiz/ascii-image-converter) binary for your system on first run.

Clone the repository:
```bash
git clone https://github.com/widkit/greetings
```
cd into `greetings`:

```bash
cd greetings
```
Install dependencies via pip:

```bash
pip install -r requirements.txt
```

## Using the script
```bash
python3 src/main.py
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
/path/to/greetings-linux  # or greetings-macos

# If using Python script:
python "/path/to/src/main.py"
```

## Tips

- You can save the daily images by setting `save_images = True` in ~/.config/greetings/greetings.yaml
- Images are cached in ~/.config/greetings/ to avoid unnecessary downloads.

## Customization

You can change the parameters of `ascii-image-converter` in src/main.py to alter the output. Here are some useful flags:

```
ascii-image-converter [image paths/urls or piped stdin] [flags]

Common flags:
  -C, --color             Display ascii art with original colors
  -b, --braille          Use braille characters instead of ascii
  -d, --dimensions       Set width and height (e.g. -d 60,30)
  -f, --full            Use largest dimensions that fill terminal width
  -g, --grayscale       Display grayscale ascii art
  -c, --complex         Display ascii characters in larger range
```

For all available options, see the [full manpage below](#full-manpage).

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


