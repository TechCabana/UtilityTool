import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QComboBox, QMessageBox
from utils import generate_rename_pattern

class FileToolsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📂 File Tools"))

        self.select_btn = QPushButton("Select Files")
        self.select_btn.clicked.connect(self.select_files)
        layout.addWidget(self.select_btn)

        self.pattern_box = QComboBox()
        self.pattern_box.addItems(["default", "date", "regex"])
        layout.addWidget(self.pattern_box)

        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("Suffix (optional)")
        layout.addWidget(self.suffix_input)

        rename_btn = QPushButton("Rename Files")
        rename_btn.clicked.connect(self.rename_files)
        layout.addWidget(rename_btn)

        self.setLayout(layout)
        self.files = []

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        if files:
            self.files = files

    def rename_files(self):
        if not self.files:
            QMessageBox.warning(self, "No files", "Please select files first.")
            return
        for file_path in self.files:
            folder = os.path.dirname(file_path)
            new_name = generate_rename_pattern(os.path.basename(file_path), self.pattern_box.currentText(), self.suffix_input.text())
            os.rename(file_path, os.path.join(folder, new_name))
        QMessageBox.information(self, "Done", "Files renamed successfully!")
