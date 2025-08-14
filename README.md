# Local Utility Application

## Setup Instructions

### 1. Install Python
Make sure Python 3.9+ is installed. On macOS, use:
```
brew install python
```

On Windows, download from python.org and check 'Add Python to PATH'.

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run in Visual Studio Code
- Open folder in VS Code
- Install Python extension
- Press F5 to run in Debug Mode

### 4. Compile for macOS
```
pip install pyinstaller
pyinstaller --onefile --windowed main.py --name 'LocalUtility'
mv dist/LocalUtility.app /Applications/
```

### 5. Compile for Windows
```
pip install pyinstaller
pyinstaller --onefile --windowed main.py --name LocalUtility
move dist\LocalUtility.exe "C:\Program Files\LocalUtility\"
```

