from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QListWidget, 
    QHBoxLayout, QLineEdit, QSpinBox, QComboBox, QMessageBox
)
from file_utils import batch_preview, apply_renames

class FileToolsTab(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout()
        head = QLabel("📁 File Tools — Batch Rename")
        head.setStyleSheet("font-size:16px; font-weight:bold;")
        root.addWidget(head)

        self.listw = QListWidget()
        root.addWidget(self.listw)

        row1 = QHBoxLayout()
        add_btn = QPushButton("Add Files"); add_btn.clicked.connect(self.add_files)
        clear_btn = QPushButton("Clear"); clear_btn.clicked.connect(self.listw.clear)
        row1.addWidget(add_btn); row1.addWidget(clear_btn)
        root.addLayout(row1)

        # options
        row2 = QHBoxLayout()
        self.prefix = QLineEdit(); self.prefix.setPlaceholderText("Prefix (supports {date} / {num})")
        self.suffix = QLineEdit(); self.suffix.setPlaceholderText("Suffix")
        self.start = QSpinBox(); self.start.setRange(0, 999999); self.start.setValue(1); self.start.setToolTip("Start number for {num}")
        self.pad = QSpinBox(); self.pad.setRange(1, 6); self.pad.setValue(2); self.pad.setToolTip("Zero padding for {num}")
        self.case = QComboBox(); self.case.addItems(["none", "lower", "upper", "title"])
        row2.addWidget(self.prefix); row2.addWidget(self.suffix); row2.addWidget(self.start); row2.addWidget(self.pad); row2.addWidget(self.case)
        root.addLayout(row2)

        row3 = QHBoxLayout()
        self.regex_find = QLineEdit(); self.regex_find.setPlaceholderText("Regex find (optional)")
        self.regex_replace = QLineEdit(); self.regex_replace.setPlaceholderText("Replace")
        self.date_source = QComboBox(); self.date_source.addItems(["now", "file_modified"])
        row3.addWidget(self.regex_find); row3.addWidget(self.regex_replace); row3.addWidget(self.date_source)
        root.addLayout(row3)

        # actions
        prev = QPushButton("Preview"); prev.clicked.connect(self.preview)
        apply = QPushButton("Apply"); apply.clicked.connect(self.apply)
        root.addWidget(prev); root.addWidget(apply)

        self.preview_list = QListWidget()
        root.addWidget(QLabel("Preview:"))
        root.addWidget(self.preview_list)

        self.setLayout(root)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        for f in files:
            self.listw.addItem(f)

    def preview(self):
        files = [self.listw.item(i).text() for i in range(self.listw.count())]
        if not files:
            QMessageBox.warning(self, "No files", "Add files first")
            return
        # Build combined prefix with tokens (we let token replacement happen in utils)
        prefix = self.prefix.text()
        suffix = self.suffix.text()

        previews = batch_preview(
            files,
            prefix=prefix,
            suffix=suffix,
            start=self.start.value(),
            pad=self.pad.value(),
            date_source=self.date_source.currentText(),
            regex_find=(self.regex_find.text() or None),
            regex_replace=(self.regex_replace.text() or None),
            case=self.case.currentText(),
            numbering="{num}" in prefix or "{num}" in "".join(files) or True  # enable numbering if requested; fall back to True so 'start' works
        )
        self.preview_list.clear()
        for p in previews:
            self.preview_list.addItem(p)

    def apply(self):
        files = [self.listw.item(i).text() for i in range(self.listw.count())]
        previews = [self.preview_list.item(i).text() for i in range(self.preview_list.count())]
        if not files or not previews or len(files) != len(previews):
            QMessageBox.warning(self, "No preview", "Generate preview first")
            return
        apply_renames(files, previews)
        QMessageBox.information(self, "Done", "Renames applied.")
