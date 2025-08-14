import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PIL import Image
from utils import get_passport_size

class ImageWorker(QThread):
    progress = pyqtSignal(int, str)

    def __init__(self, files, resize=None, format=None):
        super().__init__()
        self.files = files
        self.resize = resize
        self.format = format

    def run(self):
        total = len(self.files)
        for i, file_path in enumerate(self.files):
            try:
                img = Image.open(file_path)
                if self.resize:
                    img = img.resize(self.resize)
                save_path = os.path.splitext(file_path)[0] + "_converted"
                if self.format:
                    save_path += f".{self.format.lower()}"
                    img.save(save_path, self.format)
                else:
                    img.save(save_path + ".jpg", "JPEG")
                self.progress.emit(int((i + 1) / total * 100), file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

class ImageToolsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🖼 Image Tools"))

        self.select_btn = QPushButton("Select Images")
        self.select_btn.clicked.connect(self.select_images)
        layout.addWidget(self.select_btn)

        self.format_box = QComboBox()
        self.format_box.addItems(["JPEG", "PNG", "BMP", "TIFF"])
        layout.addWidget(self.format_box)

        self.passport_box = QComboBox()
        self.passport_box.addItems(["None", "India", "Netherlands"])
        layout.addWidget(self.passport_box)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self.convert_images)
        layout.addWidget(convert_btn)

        self.setLayout(layout)
        self.files = []

    def select_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp *.tiff)")
        if files:
            self.files = files

    def convert_images(self):
        if not self.files:
            QMessageBox.warning(self, "No files", "Please select images first.")
            return
        resize = None
        if self.passport_box.currentText() != "None":
            resize = get_passport_size(self.passport_box.currentText())
        self.worker = ImageWorker(self.files, resize=resize, format=self.format_box.currentText())
        self.worker.progress.connect(self.update_progress)
        self.worker.start()

    def update_progress(self, value, filename):
        self.progress_bar.setValue(value)
