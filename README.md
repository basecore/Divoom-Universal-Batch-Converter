# Divoom Universal Batch Converter 👾 (Web App)

A completely client-side, browser-based tool designed to convert images and animations into the strict GIF format required by Divoom pixel art displays. 

This project was specifically created as a companion tool for the awesome [esp32-divoom](https://github.com/d03n3rfr1tz3/esp32-divoom) and [hass-divoom](https://github.com/d03n3rfr1tz3/hass-divoom) Home Assistant integrations.

## 🚀 Try it out right now!
**[Click here to open the Web App](https://basecore.github.io/Divoom-Universal-Batch-Converter/)**  
*(Note: Ensure your GitHub Pages settings point to the `main` branch to use this link)*

## 🤖 Built with AI (Gemini 3.1 Pro)
I actually don't have any programming skills! I built this entire tool from scratch using **Gemini 3.1 Pro**. 
Why? I just wanted a simple, reliable way to get my GIFs working perfectly on my ESP32 Divoom Pixoo. I was tired of relying on external, ad-riddled conversion websites that might secretly store user data, and I didn't want to install any software on my PC. I needed something that works *on the fly*, directly in the browser, and can be hosted securely and freely via GitHub. Thanks to AI, this zero-compromise tool now exists for everyone to use!

## ⚠️ The Problem it Solves
As discussed in [hass-divoom Issue #19](https://github.com/d03n3rfr1tz3/hass-divoom/issues/19), simply downloading a GIF from the Divoom app or the web and sending it to your device via Home Assistant often fails (e.g., showing only a solid background color, flickering colors, or rendering as a blurry mess). 

Divoom hardware is highly specific and requires GIFs to be:
1. **Exactly the size of the display** (e.g., 16x16, 32x32, or 64x64 pixels) – *not* the 320x320 size exported by the Divoom App.
2. **Non-interlaced**.
3. Saved with a **True Global Color Palette** (crucial to prevent color shifting/flickering across frames).
4. Scaled without interpolation (**Nearest Neighbor**) to retain hard pixel-art edges.

This web app runs entirely in your browser and automates this formatting process instantly.

## ✨ Key Features
* **True Global Palette Engine:** Analyzes all frames simultaneously to generate a single, strict color palette. This entirely eliminates the "flickering background" issue commonly seen when scaling animated pixel art.
* **Precision Point Sampling:** Uses a mathematically perfect Nearest-Neighbor algorithm (similar to `gifsicle`) that ignores grid lines and anti-aliasing artifacts, sampling only the pure center color of each pixel block.
* **Interactive Visual Grid:** An overlaid real-time red grid shows you exactly where the algorithm is sampling data, allowing you to perfectly tune the offset to match your source image's grid.
* **No Installation Required:** Runs directly in your browser.
* **100% Private:** Your files are processed locally via WebAssembly and JavaScript. Nothing is ever uploaded to a server.
* **Format Agnostic:** Converts `.gif`, `.webp`, `.png`, and `.jpg` into the correct Divoom-ready `.gif` format.
* **Batch Processing:** Drop a whole folder with 100 images, and the app will generate a single `.zip` file containing 100 perfectly scaled GIFs.

## 🔧 Supported Devices
Select your device from the dropdown before dropping your files:
* **10x10:** Aurabox
* **11x11:** Timebox Mini
* **16x16:** Pixoo, Pixoo Backpack, Ditoo, Ditoo Mic, Timebox, Timebox Evo, Timoo, Tivoo
* **32x32:** Pixoo Max, Backpack M
* **64x64:** Pixoo 64

## 🏡 Using your GIFs in Home Assistant
Once you have converted your GIFs using this tool, you can easily display them on your Divoom device using the [hass-divoom](https://github.com/d03n3rfr1tz3/hass-divoom) integration. 

### 1. Create the Media Directory & Upload your GIFs
1. Open your Home Assistant configuration directory (this is the root folder where your `configuration.yaml` is located).
2. Create a new folder named `pixelart` inside this directory. 
   *(Note: The downloaded `hass-divoom` ZIP file includes a `pixelart` folder with some sample images that you could copy over. However, if you don't want to use their sample content, simply create an empty folder named `pixelart` manually).*
3. Upload your perfectly converted `.gif` files directly into this new `pixelart` folder.

### 2. Configure the Notify Service
If you haven't already, install the `hass-divoom` custom component manually (by copying the downloaded zip contents into `custom_components\divoom`). 
Then, add the following snippet to your `configuration.yaml` to set up the notify service for your device:

```yaml
notify:
  - name: Divoom Device
    platform: divoom
    # host: "192.168.0.123"      # Optional: IP of your ESP32 Bluetooth Proxy
    mac: "12:34:56:78:9A"        # Required: Bluetooth MAC address of your Divoom
    port: 1                      # Optional: Usually 1 (might be 2 for devices with audio)
    device_type: "pixoo"         # Required: e.g., pixoo, ditoo, timebox, etc.
    media_directory: "pixelart"  # Required: The directory you created in Step 1
    escape_payload: false        # Optional: Set to true only for some older Divoom firmwares
```

### 3. Send the Image to your Divoom
You can now display your uploaded GIFs by calling the notify service (e.g., in automations, scripts, or the Developer Tools). Simply use the `image` mode and specify the filename:

```yaml
service: notify.divoom_device
data:
  message: "image"
  data:
    file: "your_converted_animation.gif" # Must match the exact filename in your pixelart folder
    # time: 100 # Optional: Time in ms between frames. Defaults to the GIF's native timing.
```

## ⚙️ How to host this yourself (for forks)
Since this is a static HTML app without a backend, hosting it is incredibly easy:
1. Fork or clone this repository.
2. Go to your repository settings on GitHub.
3. Navigate to **Pages**.
4. Under "Build and deployment", set the source to **Deploy from a branch** and select the `main` branch.
5. Save, wait a minute, and your site is live!

## 🧠 Under the Hood
This tool relies on modern web technologies to process images natively:
* [gifuct-js](https://github.com/matt-way/gifuct-js) for parsing and decompressing complex GIF disposal methods.
* [gifenc](https://github.com/mattdesl/gifenc) for highly optimized, global-palette GIF encoding directly in the browser.
* [JSZip](https://stuk.github.io/jszip/) for client-side batching.

## ❤️ Acknowledgements
Huge thanks to [@d03n3rfr1tz3](https://github.com/d03n3rfr1tz3) for creating the ESP32 Divoom integration that makes custom smart home pixel art possible!
