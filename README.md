# Divoom Universal Batch Converter 👾

A lightweight, cross-platform GUI tool designed to convert images and animations into the strict GIF format required by Divoom pixel art displays. 

This project was specifically created as a companion tool for the awesome [esp32-divoom](https://github.com/d03n3rfr1tz3/esp32-divoom) and [hass-divoom](https://github.com/d03n3rfr1tz3/hass-divoom) Home Assistant integrations.

## ⚠️ The Problem it Solves
As discussed in [hass-divoom Issue #19](https://github.com/d03n3rfr1tz3/hass-divoom/issues/19), simply downloading a GIF from the Divoom app or the web and sending it to your device via Home Assistant often fails (e.g., showing only a solid background color). 

Divoom hardware is highly specific and requires GIFs to be:
1. **Exactly the size of the display** (e.g., 16x16 or 32x32 pixels) – *not* the 320x320 size exported by the Divoom App.
2. **Non-interlaced**.
3. Saved with a **global color palette**.
4. Scaled without interpolation (Nearest Neighbor) to keep the hard pixel-art look instead of a blurry mess.

While you can do this manually in GIMP, this tool automates the entire process for bulk conversions.

## ✨ Features
* **Drag & Drop:** Just drop single files or entire folders into the app.
* **Format Agnostic:** Converts `.gif`, `.webp`, `.avif`, `.png`, `.jpg`, and `.jpeg` into the correct Divoom-ready `.gif` format.
* **Batch Processing:** Drop a folder with 100 images, get 100 Divoom-ready GIFs in seconds.
* **Live Preview:** Side-by-side preview of your original file and the actual hard-scaled, pixel-perfect result.
* **Auto-Dependencies:** The script automatically installs required Python modules on first launch.
* **Cross-Platform:** Works on Windows, macOS, and Linux (including modern environments with PEP 668 restrictions like Linux Mint/Ubuntu).

## 🚀 Supported Devices
Select your device from the dropdown before dropping your files:
* **10x10:** Aurabox
* **11x11:** Timebox Mini
* **16x16:** Pixoo, Pixoo Backpack, Ditoo, Ditoo Mic, Timebox, Timebox Evo, Timoo, Tivoo
* **32x32:** Pixoo Max, Backpack M
* **64x64:** Pixoo 64

## 🛠️ How to Use

### Prerequisites
* [Python 3](https://www.python.org/downloads/) installed on your system.

### Running the Tool
1. Download or clone this repository.
2. Open your terminal / command prompt.
3. Run the script:
   ```bash
   python divoom_converter.py
(Note: On Mac/Linux, you might need to use python3 divoom_converter.py)
4. The script will automatically install Pillow, pillow-avif-plugin, and PyQt6 if they are missing.
5. Select your device, choose where to save the files, and drop your media!

# 📸 Screenshots
(Upload a screenshot of the running GUI and link it here: ![Screenshot](link-to-image.png))

# ❤️ Acknowledgements
Huge thanks to @d03n3rfr1tz3 for creating the ESP32 Divoom integration that makes custom smart home pixel art possible!
