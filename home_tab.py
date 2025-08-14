from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox

class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🏠 Home - Global Settings & Presets"))
        
        save_preset_btn = QPushButton("Save Preset")
        save_preset_btn.clicked.connect(self.save_preset)
        layout.addWidget(save_preset_btn)

        self.setLayout(layout)

    def save_preset(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Preset", "", "Preset Files (*.preset)")
        if path:
            with open(path, "w") as f:
                f.write("preset_data_example")
            QMessageBox.information(self, "Preset Saved", f"Preset saved at: {path}")
