# Utility Tool

A simple cross-platform Python application with a dark theme UI for:
- **Image Tools**: convert formats, resize (including passport sizes for India & Netherlands), compress with quality preview, drag & drop, progress bars, ETA display.
- **File Tools**: batch rename with prefixes, suffixes, numbering, `{date}`, regex support, preview.
- **Home Tab**: manage global settings and presets.

---

## 📦 Requirements

Before running or building the app, ensure you have:

- **Python 3.9+** installed
- **Pip** (comes with Python)
- **VS Code** with Python extension
- **PyInstaller** (`pip install pyinstaller`)
- **Dependencies**: install via  
  ```bash
  pip install -r requirements.txt
  ```

---

## 💻 1. Running the App in VS Code

1. **Open Project in VS Code**  
   - Launch VS Code  
   - Go to `File → Open Folder…` and select the folder containing the app files.

2. **Install Dependencies**  
   Open the **Terminal** in VS Code (`Ctrl+`` or `Cmd+``) and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**  
   Press **F5** (or go to *Run → Start Debugging*) and choose **Python File**.  
   The app window should open.

---

## 🍏 2. macOS — Building a Standalone `.app`

1. **Install PyInstaller**  
   ```bash
   pip install pyinstaller
   ```

2. **Build the App**  
   From the project root folder in VS Code terminal:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --name "Utility Tool" main.py
   ```

3. **Locate the Build Output**  
   The `.app` file will be in:
   ```
   dist/Utility Tool.app
   ```

4. **Move to Applications Folder**  
   Drag the `.app` into your **Applications** folder.

---

## 🪟 3. Windows — Building a Standalone `.exe`

1. **Install PyInstaller**  
   ```bash
   pip install pyinstaller
   ```

2. **Build the App**  
   From the project root folder in VS Code terminal:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --name "Utility Tool" main.py
   ```

3. **Locate the Build Output**  
   The `.exe` file will be in:
   ```
   dist\Utility Tool.exe
   ```

4. **Move to Program Files Folder**  
   Copy the `.exe` into `C:\Program Files\Utility Tool\` (create folder if needed).

---

## ⚠️ Notes

- **macOS Security**: The first time you run the `.app`, you may need to right-click and choose “Open” to bypass Gatekeeper.
- **Windows SmartScreen**: You may need to click “Run anyway” on first launch.
- If the app doesn’t launch, ensure **PyQt5** and **Pillow** are installed:
  ```bash
  pip install PyQt5 Pillow
  ```
