import sys
import os
import io
import subprocess

# --- 1. Auto-Installation of missing modules (Cross-Platform) ---
def install_and_import():
    missing = []
    try:
        import PIL
    except ImportError:
        missing.append('Pillow')
    
    try:
        import pillow_avif
    except ImportError:
        missing.append('pillow-avif-plugin') # Required for AVIF support

    try:
        import PyQt6
    except ImportError:
        missing.append('PyQt6')

    if missing:
        print(f"Installing missing modules: {', '.join(missing)}...")
        try:
            cmd = [sys.executable, "-m", "pip", "install"] + missing
            # Override PEP 668 for modern Linux environments (e.g., Linux Mint/Ubuntu)
            if sys.platform == "linux":
                cmd.append("--break-system-packages")
            subprocess.check_call(cmd)
            print("Installation successful!")
        except Exception as e:
            print(f"
Error during automatic installation: {e}")
            if sys.platform == "linux":
                print("
Please install the packages manually via terminal on Linux:")
                print("sudo apt update && sudo apt install python3-pyqt6 python3-pil")
                print("pip install pillow-avif-plugin --break-system-packages")
            sys.exit(1)

install_and_import()

# --- 2. Main Application ---
from PIL import Image, ImageSequence
import pillow_avif # Must be imported so Pillow registers the AVIF format
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, 
                             QWidget, QListWidget, QListWidgetItem, QComboBox, QGroupBox,
                             QRadioButton, QLineEdit, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt, QByteArray, QBuffer, QIODevice
from PyQt6.QtGui import QColor, QMovie

# Supported input formats
SUPPORTED_FORMATS = ('.gif', '.png', '.jpg', '.jpeg', '.webp', '.avif')

# Definition of Divoom models and target dimensions
DEVICE_SIZES = {
    "Pixoo / Pixoo Backpack (16x16)": (16, 16),
    "Ditoo / Ditoo Mic (16x16)": (16, 16),
    "Timebox / Timebox Evo (16x16)": (16, 16),
    "Timoo (16x16)": (16, 16),
    "Tivoo (16x16)": (16, 16),
    "Timebox Mini (11x11)": (11, 11),
    "Aurabox (10x10)": (10, 10),
    "Pixoo Max / Backpack M (32x32)": (32, 32),
    "Pixoo 64 (64x64)": (64, 64)
}

def convert_for_divoom(input_path, output_path, target_size):
    try:
        img = Image.open(input_path)

        frames = []
        orig_preview_frames = []
        conv_preview_frames = []
        durations = []

        scale_factor = 256 // target_size[0]
        preview_size = (target_size[0] * scale_factor, target_size[1] * scale_factor)

        # Iterate over all frames (static images like JPG only have 1 frame)
        for frame in ImageSequence.Iterator(img):
            durations.append(frame.info.get('duration', 100))
            frame_rgba = frame.convert("RGBA")
            
            # 1. Target frame (e.g. 16x16, Nearest Neighbor for crisp pixel-art look)
            out_f = frame_rgba.resize(target_size, Image.Resampling.NEAREST)
            frames.append(out_f)
            
            # 2. Original preview frame (256x256, smoothly scaled for GUI)
            orig_p = frame_rgba.resize(preview_size, Image.Resampling.LANCZOS)
            orig_preview_frames.append(orig_p)
            
            # 3. Converted preview frame (256x256, hard scaled for GUI to simulate pixels)
            conv_p = out_f.resize(preview_size, Image.Resampling.NEAREST)
            conv_preview_frames.append(conv_p)

        loop_count = img.info.get('loop', 0)

        # 1. Save file to disk as Divoom-ready GIF
        frames[0].save(
            output_path,
            format='GIF',
            save_all=True,
            append_images=frames[1:] if len(frames) > 1 else [],
            duration=durations,
            loop=loop_count,
            interlace=False, # Crucial requirement for Divoom
            disposal=2       # Prevents ghosting with transparency
        )

        # 2. Generate 'Original' preview in RAM for GUI
        orig_buffer = io.BytesIO()
        orig_preview_frames[0].save(
            orig_buffer, format='GIF', save_all=True,
            append_images=orig_preview_frames[1:] if len(orig_preview_frames) > 1 else [],
            duration=durations, loop=loop_count, disposal=2
        )
        orig_preview_data = orig_buffer.getvalue()

        # 3. Generate 'Converted' preview in RAM for GUI
        conv_buffer = io.BytesIO()
        conv_preview_frames[0].save(
            conv_buffer, format='GIF', save_all=True,
            append_images=conv_preview_frames[1:] if len(conv_preview_frames) > 1 else [],
            duration=durations, loop=loop_count, disposal=2
        )
        conv_preview_data = conv_buffer.getvalue()

        return True, output_path, orig_preview_data, conv_preview_data
    except Exception as e:
        return False, str(e), None, None

# --- 3. GUI Layout & Logic ---
class DropZone(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        # Keep references for Garbage Collector so animations keep playing
        self.movie_orig = None
        self.movie_conv = None
        self.preview_buffer_orig = None
        self.qbuffer_orig = None
        self.preview_buffer_conv = None
        self.qbuffer_conv = None
        
        main_layout = QVBoxLayout()
        
        # --- Section 1: Divoom Models ---
        self.combo_box = QComboBox()
        self.combo_box.addItems(list(DEVICE_SIZES.keys()))
        self.combo_box.setStyleSheet("font-size: 14px; padding: 5px;")
        
        device_group = QGroupBox("1. Select Divoom Device / Target Size")
        device_group.setStyleSheet("font-weight: bold;")
        vbox_device = QVBoxLayout()
        vbox_device.addWidget(self.combo_box)
        device_group.setLayout(vbox_device)
        
        # --- Section 2: Output Location ---
        output_group = QGroupBox("2. Select Output Location")
        output_group.setStyleSheet("font-weight: bold;")
        vbox_out = QVBoxLayout()
        
        self.radio_same = QRadioButton("Save in the same folder (suffix added to filename)")
        self.radio_custom = QRadioButton("Save in a custom folder:")
        self.radio_same.setChecked(True)
        self.radio_same.setStyleSheet("font-weight: normal;")
        self.radio_custom.setStyleSheet("font-weight: normal;")
        
        hbox_custom_path = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setEnabled(False)
        self.path_input.setStyleSheet("font-weight: normal;")
        
        self.btn_browse = QPushButton("Browse...")
        self.btn_browse.setEnabled(False)
        self.btn_browse.setStyleSheet("font-weight: normal;")
        
        hbox_custom_path.addWidget(self.path_input)
        hbox_custom_path.addWidget(self.btn_browse)
        
        vbox_out.addWidget(self.radio_same)
        vbox_out.addWidget(self.radio_custom)
        vbox_out.addLayout(hbox_custom_path)
        output_group.setLayout(vbox_out)
        
        self.radio_same.toggled.connect(self.toggle_output_options)
        self.btn_browse.clicked.connect(self.browse_folder)
        
        # --- Section 3: Drag & Drop ---
        self.drop_label = QLabel(f"3. Drop images/animations or entire folders here
Supported: {', '.join(SUPPORTED_FORMATS)}")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 3px dashed #888; border-radius: 15px; font-size: 16px;
                color: #555; background-color: #f0f0f0; min-height: 80px; margin: 5px 0px;
                font-weight: bold;
            }
        """)
        
        # --- Section 4: Preview ---
        preview_group = QGroupBox("4. Preview (Last processed image)")
        preview_group.setStyleSheet("font-weight: bold;")
        preview_layout = QHBoxLayout()
        
        vbox_orig = QVBoxLayout()
        lbl_orig_title = QLabel("Original")
        lbl_orig_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_orig_title.setStyleSheet("font-weight: normal;")
        self.lbl_orig_img = QLabel("No Image")
        self.lbl_orig_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_orig_img.setFixedSize(256, 256)
        self.lbl_orig_img.setStyleSheet("background-color: #e0e0e0; border: 1px solid #ccc; font-weight: normal;")
        vbox_orig.addWidget(lbl_orig_title)
        vbox_orig.addWidget(self.lbl_orig_img)
        
        vbox_conv = QVBoxLayout()
        lbl_conv_title = QLabel("Converted as GIF (Pixel-Perfect)")
        lbl_conv_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_conv_title.setStyleSheet("font-weight: normal;")
        self.lbl_conv_img = QLabel("No Image")
        self.lbl_conv_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_conv_img.setFixedSize(256, 256)
        self.lbl_conv_img.setStyleSheet("background-color: #e0e0e0; border: 1px solid #ccc; font-weight: normal;")
        vbox_conv.addWidget(lbl_conv_title)
        vbox_conv.addWidget(self.lbl_conv_img)
        
        preview_layout.addLayout(vbox_orig)
        preview_layout.addLayout(vbox_conv)
        preview_group.setLayout(preview_layout)
        
        # --- Section 5: Status & Logs ---
        self.list_widget = QListWidget()
        self.list_widget.setFixedHeight(120)
        self.list_widget.setStyleSheet("font-size: 13px; font-weight: normal;")
        
        main_layout.addWidget(device_group)
        main_layout.addWidget(output_group)
        main_layout.addWidget(self.drop_label)
        main_layout.addWidget(preview_group)
        main_layout.addWidget(self.list_widget)
        self.setLayout(main_layout)

    def toggle_output_options(self):
        is_custom = self.radio_custom.isChecked()
        self.path_input.setEnabled(is_custom)
        self.btn_browse.setEnabled(is_custom)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Target Folder")
        if folder:
            self.path_input.setText(folder)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_label.setStyleSheet(self.drop_label.styleSheet().replace("#888", "#4CAF50").replace("#f0f0f0", "#e8f5e9"))
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.drop_label.setStyleSheet(self.drop_label.styleSheet().replace("#4CAF50", "#888").replace("#e8f5e9", "#f0f0f0"))

    def dropEvent(self, event):
        self.dragLeaveEvent(event)
        
        if self.radio_custom.isChecked() and not self.path_input.text():
            self.add_log("❌ Aborted: Please select a target folder first!", "#c62828")
            return

        urls = event.mimeData().urls()
        target_size = DEVICE_SIZES[self.combo_box.currentText()]
        custom_folder = self.path_input.text() if self.radio_custom.isChecked() else None
        
        # Gather all valid files
        files_to_process = []
        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(SUPPORTED_FORMATS):
                            files_to_process.append(os.path.join(root, file))
            elif path.lower().endswith(SUPPORTED_FORMATS):
                files_to_process.append(path)

        if not files_to_process:
            self.add_log("⚠️ No supported images or animations found.", "#ef6c00")
            return

        self.add_log(f"🔄 Starting batch processing for {len(files_to_process)} file(s)...", "#1565c0")
        QApplication.processEvents()

        success_count = 0
        error_count = 0

        for file_path in files_to_process:
            # Generate output path (always enforces .gif extension)
            name, _ = os.path.splitext(os.path.basename(file_path))
            suffix = f"_{target_size[0]}x{target_size[1]}"
            out_filename = f"{name}{suffix}.gif"
            
            if custom_folder:
                out_path = os.path.join(custom_folder, out_filename)
            else:
                out_path = os.path.join(os.path.dirname(file_path), out_filename)

            success, result_path, orig_data, conv_data = convert_for_divoom(file_path, out_path, target_size)
            
            if success:
                self.add_log(f"✅ {os.path.basename(result_path)}", "#2e7d32")
                self.update_previews(orig_data, conv_data)
                success_count += 1
            else:
                self.add_log(f"❌ Error at {os.path.basename(file_path)}: {result_path}", "#c62828")
                error_count += 1
                
            QApplication.processEvents()

        self.add_log(f"🏁 Finished: {success_count} successful, {error_count} failed.", "#1565c0")

    def update_previews(self, orig_data, conv_data):
        # 1. Original preview (from RAM)
        self.preview_buffer_orig = QByteArray(orig_data)
        self.qbuffer_orig = QBuffer(self.preview_buffer_orig)
        self.qbuffer_orig.open(QIODevice.OpenModeFlag.ReadOnly)
        self.movie_orig = QMovie()
        self.movie_orig.setDevice(self.qbuffer_orig)
        self.lbl_orig_img.setMovie(self.movie_orig)
        self.movie_orig.start()
        
        # 2. Converted preview (from RAM)
        self.preview_buffer_conv = QByteArray(conv_data)
        self.qbuffer_conv = QBuffer(self.preview_buffer_conv)
        self.qbuffer_conv.open(QIODevice.OpenModeFlag.ReadOnly)
        self.movie_conv = QMovie()
        self.movie_conv.setDevice(self.qbuffer_conv)
        self.lbl_conv_img.setMovie(self.movie_conv)
        self.movie_conv.start()

    def add_log(self, text, color_hex):
        item = QListWidgetItem(text)
        item.setForeground(QColor(color_hex))
        self.list_widget.addItem(item)
        self.list_widget.scrollToBottom()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Divoom Universal Batch Converter")
        self.resize(650, 800)
        self.setCentralWidget(DropZone())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
