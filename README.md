# greetings

![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python program that works on Mac, Linux and Windows which fetches the daily Bing wallpaper and converts it into colorful ASCII art. It may be used with shells as a color script, as seen in DistroTube's Youtube channel.

## Dependencies

* [ascii-image-converter](https://github.com/TheZoraiz/ascii-image-converter)
* [requests](https://pypi.org/project/requests/)
* [pytz](https://github.com/stub42/pytz)

## Recommended
* Terminal supporting 24-bit or 8-bit color (Highly Recommended)
  

## Installation
Install `requests` and `pytz` via pip:

```bash
pip install requests pytz
```
Install ascii-image-converter:
[ascii-image-converter](https://github.com/TheZoraiz/ascii-image-converter)


 Clone the repository:
 ```bash
git clone https://github.com/widkit/greetings
```
## Using the script
 ```bash
cd greetings
```
 ```bash
python3 main.py
```

## Using as a color script (runs at shell start-up)
# Windows
Create and edit a PowerShell profile:
```
notepad $PROFILE
```
Add the following line at the top:
```
python "PATH-TO-FILE.py"
```
Replace the path with the file path itself.
# Unix (Mac, Linux)
Add line to your shell profile:
```
python "PATH-TO-FILE.py"
```

## Tips

- You can save the daily images by uncommenting `save_images = True` at line 8.

- You can change the value of `ascii-image-converter` in line 56 of `main.py`, which alters the output.
  Here's the manual for `ascii-image-converter`:
  
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

