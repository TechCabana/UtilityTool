import os, json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, 
    QHBoxLayout, QFileDialog, QMessageBox, QComboBox, QCheckBox
)

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".utilitytool")
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.json")
PRESETS_PATH = os.path.join(CONFIG_DIR, "presets.json")

DEFAULT_SETTINGS = {
    "theme": "dark",
    "default_output": "",
    "default_format": "JPEG",
    "default_quality": 85,
    "preserve_exif": False,
    "remember_last": True
}

def ensure_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "w") as f: json.dump(DEFAULT_SETTINGS, f, indent=2)
    if not os.path.exists(PRESETS_PATH):
        with open(PRESETS_PATH, "w") as f: json.dump({"presets": {}}, f, indent=2)

class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        ensure_config()
        self.settings = self._load_json(SETTINGS_PATH)
        self.presets = self._load_json(PRESETS_PATH)

        root = QVBoxLayout()
        title = QLabel("🏠 Home — Global Settings & Presets")
        title.setStyleSheet("font-size:16px; font-weight:bold;")
        root.addWidget(title)

        form = QFormLayout()
        self.theme = QComboBox(); self.theme.addItems(["dark", "light", "system"])
        self.theme.setCurrentText(self.settings.get("theme", "dark"))

        self.default_output = QLineEdit(self.settings.get("default_output", ""))
        self.default_format = QComboBox(); self.default_format.addItems(["JPEG","PNG","WEBP","TIFF","BMP"])
        self.default_format.setCurrentText(self.settings.get("default_format", "JPEG"))

        self.default_quality = QLineEdit(str(self.settings.get("default_quality", 85)))
        self.preserve_exif = QCheckBox(); self.preserve_exif.setChecked(self.settings.get("preserve_exif", False))
        self.remember_last = QCheckBox(); self.remember_last.setChecked(self.settings.get("remember_last", True))

        form.addRow("Theme:", self.theme)
        form.addRow("Default Output Folder:", self.default_output)
        form.addRow("Default Format:", self.default_format)
        form.addRow("Default Quality (1–100):", self.default_quality)
        form.addRow("Preserve EXIF:", self.preserve_exif)
        form.addRow("Remember last settings:", self.remember_last)
        root.addLayout(form)

        browse_row = QHBoxLayout()
        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._pick_output)
        browse_row.addWidget(browse_btn)
        root.addLayout(browse_row)

        # Presets: Save current format/quality under a name
        root.addWidget(QLabel("Presets (format + quality):"))
        p_row = QHBoxLayout()
        self.preset_name = QLineEdit(); self.preset_name.setPlaceholderText("Preset name (e.g., JPEG-85-Web)")
        save_btn = QPushButton("Save Preset"); save_btn.clicked.connect(self._save_preset)
        load_btn = QPushButton("Load Preset"); load_btn.clicked.connect(self._load_preset)
        export_btn = QPushButton("Export Presets"); export_btn.clicked.connect(self._export_presets)
        import_btn = QPushButton("Import Presets"); import_btn.clicked.connect(self._import_presets)
        p_row.addWidget(self.preset_name); p_row.addWidget(save_btn); p_row.addWidget(load_btn); p_row.addWidget(export_btn); p_row.addWidget(import_btn)
        root.addLayout(p_row)

        actions = QHBoxLayout()
        save_settings = QPushButton("Save Settings"); save_settings.clicked.connect(self._save_settings)
        reset = QPushButton("Reset to Defaults"); reset.clicked.connect(self._reset_defaults)
        actions.addWidget(save_settings); actions.addWidget(reset)
        root.addLayout(actions)

        self.setLayout(root)

    # Helpers
    def _load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def _write_json(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def _pick_output(self):
        path = QFileDialog.getExistingDirectory(self, "Choose default output folder")
        if path:
            self.default_output.setText(path)

    def _save_settings(self):
        try:
            data = {
                "theme": self.theme.currentText(),
                "default_output": self.default_output.text(),
                "default_format": self.default_format.currentText(),
                "default_quality": int(self.default_quality.text() or "85"),
                "preserve_exif": self.preserve_exif.isChecked(),
                "remember_last": self.remember_last.isChecked()
            }
            self._write_json(SETTINGS_PATH, data)
            QMessageBox.information(self, "Saved", "Settings saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _reset_defaults(self):
        self._write_json(SETTINGS_PATH, DEFAULT_SETTINGS)
        QMessageBox.information(self, "Reset", "Defaults restored. Reopen Home tab to reload.")

    def _save_preset(self):
        name = self.preset_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Name required", "Enter a preset name.")
            return
        self.presets["presets"][name] = {
            "default_format": self.default_format.currentText(),
            "default_quality": int(self.default_quality.text() or "85")
        }
        self._write_json(PRESETS_PATH, self.presets)
        QMessageBox.information(self, "Preset", f"Preset '{name}' saved.")

    def _load_preset(self):
        name = self.preset_name.text().strip()
        p = self.presets["presets"].get(name)
        if not p:
            QMessageBox.warning(self, "Not found", f"No preset named '{name}'.")
            return
        self.default_format.setCurrentText(p.get("default_format", "JPEG"))
        self.default_quality.setText(str(p.get("default_quality", 85)))
        QMessageBox.information(self, "Preset", f"Preset '{name}' loaded into fields.")

    def _export_presets(self):
        out, _ = QFileDialog.getSaveFileName(self, "Export presets", "presets.json", "JSON (*.json)")
        if out:
            self._write_json(out, self.presets)
            QMessageBox.information(self, "Exported", f"Presets exported to {out}")

    def _import_presets(self):
        src, _ = QFileDialog.getOpenFileName(self, "Import presets", "", "JSON (*.json)")
        if src:
            with open(src, "r") as f:
                self.presets = json.load(f)
            self._write_json(PRESETS_PATH, self.presets)
            QMessageBox.information(self, "Imported", "Presets imported.")
