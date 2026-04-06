# Divoom Universal Batch Converter 👾 (Web App)

A completely client-side, browser-based tool designed to convert images and animations into the strict GIF format required by Divoom pixel art displays. 

This project was specifically created as a companion tool for the awesome [esp32-divoom](https://github.com/d03n3rfr1tz3/esp32-divoom) and [hass-divoom](https://github.com/d03n3rfr1tz3/hass-divoom) Home Assistant integrations.

## 🚀 Try it out right now!
**[Click here to open the Web App](https://basecore.github.io/Divoom-Universal-Batch-Converter/)**
*(Note: Replace the link above with your actual GitHub Pages URL once enabled)*

## ⚠️ The Problem it Solves
As discussed in [hass-divoom Issue #19](https://github.com/d03n3rfr1tz3/hass-divoom/issues/19), simply downloading a GIF from the Divoom app or the web and sending it to your device via Home Assistant often fails (e.g., showing only a solid background color). 

Divoom hardware is highly specific and requires GIFs to be:
1. **Exactly the size of the display** (e.g., 16x16 or 32x32 pixels) – *not* the 320x320 size exported by the Divoom App.
2. **Non-interlaced**.
3. Saved with a **global color palette**.
4. Scaled without interpolation (Nearest Neighbor) to keep the hard pixel-art look instead of a blurry mess.

This web app runs entirely in your browser and automates this formatting process instantly.

## ✨ Features
* **No Installation Required:** Runs directly in your browser.
* **100% Private:** Your files are processed locally. Nothing is ever uploaded to a server.
* **Format Agnostic:** Converts `.gif`, `.webp`, `.png`, and `.jpg` into the correct Divoom-ready `.gif` format.
* **Batch Processing:** Drop a whole folder with 100 images, and the app will generate a single `.zip` file containing 100 perfectly scaled GIFs.
* **Live Preview:** Side-by-side preview of your original file and the actual hard-scaled, pixel-perfect result.

## 🔧 Supported Devices
Select your device from the dropdown before dropping your files:
* **10x10:** Aurabox
* **11x11:** Timebox Mini
* **16x16:** Pixoo, Pixoo Backpack, Ditoo, Ditoo Mic, Timebox, Timebox Evo, Timoo, Tivoo
* **32x32:** Pixoo Max, Backpack M
* **64x64:** Pixoo 64

## ⚙️ How to host this yourself (for forks)
Since this is a static HTML app without a backend, hosting it is incredibly easy:
1. Fork or clone this repository.
2. Go to your repository settings on GitHub.
3. Navigate to **Pages**.
4. Under "Build and deployment", set the source to **Deploy from a branch** and select the `main` branch.
5. Save, wait a minute, and your site is live!

## ❤️ Acknowledgements
Huge thanks to [@d03n3rfr1tz3](https://github.com/d03n3rfr1tz3) for creating the ESP32 Divoom integration that makes custom smart home pixel art possible!
