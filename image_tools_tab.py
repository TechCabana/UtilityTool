import os, time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QListWidget, QProgressBar,
    QComboBox, QHBoxLayout, QSlider, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from image_utils import convert_resize_compress, estimate_compressed_size, STANDARD_SIZES, target_dims_from_preset

# Worker thread so the UI stays responsive
class Worker(QThread):
    progress = pyqtSignal(int, str)      # overall %, filename
    perfile = pyqtSignal(int, str)       # per-file %, filename
    started_file = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, files, fmt, size_tuple, keep_aspect, quality, outdir=None):
        super().__init__()
        self.files = files
        self.fmt = fmt
        self.size = size_tuple
        self.keep_aspect = keep_aspect
        self.quality = quality
        self.outdir = outdir

    def run(self):
        total = len(self.files)
        for i, path in enumerate(self.files):
            self.started_file.emit(path)
            # Simple staged per-file progress simulation
            for step in (10, 30, 60, 90):
                self.perfile.emit(step, path)
                time.sleep(0.06)
            # Process conversion/resizing/compression
            out_path = None
            if self.outdir:
                base = os.path.splitext(os.path.basename(path))[0]
                out_path = os.path.join(self.outdir, f"{base}_out.{self.fmt.lower()}")
            convert_resize_compress(
                path, out_fmt=self.fmt, out_path=out_path,
                size=self.size, keep_aspect=self.keep_aspect, quality=self.quality
            )
            self.perfile.emit(100, path)
            pct = int(((i + 1) / total) * 100)
            self.progress.emit(pct, path)
        self.finished.emit()

class ImageToolsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.output_dir = None
        self.t0 = None

        root = QVBoxLayout()
        head = QLabel("🖼 Image Tools — Convert • Resize • Compress")
        head.setStyleSheet("font-size:16px; font-weight:bold;")
        root.addWidget(head)

        # File list (drag & drop supported by Qt at OS level when picking files — simplest path: use Add Images button)
        self.listw = QListWidget()
        self.listw.setSelectionMode(self.listw.ExtendedSelection)
        root.addWidget(self.listw)

        row = QHBoxLayout()
        add_btn = QPushButton("Add Images"); add_btn.clicked.connect(self.add_files)
        clear_btn = QPushButton("Clear"); clear_btn.clicked.connect(self.listw.clear)
        row.addWidget(add_btn); row.addWidget(clear_btn)
        root.addLayout(row)

        # Format + size preset
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Format:"))
        self.fmt = QComboBox(); self.fmt.addItems(["JPEG", "PNG", "WEBP", "TIFF", "BMP"])
        row2.addWidget(self.fmt)

        row2.addWidget(QLabel("Size Preset:"))
        self.sizepreset = QComboBox(); self.sizepreset.addItem("None")
        for k in STANDARD_SIZES.keys():
            self.sizepreset.addItem(k)
        row2.addWidget(self.sizepreset)

        self.keep_aspect = QCheckBox("Keep Aspect"); self.keep_aspect.setChecked(True)
        row2.addWidget(self.keep_aspect)
        root.addLayout(row2)

        # Compression
        comp_row = QHBoxLayout()
        comp_row.addWidget(QLabel("Quality:"))
        self.quality = QSlider(Qt.Horizontal); self.quality.setRange(1, 100); self.quality.setValue(85)
        comp_row.addWidget(self.quality)

        self.est_label = QLabel("Estimated size: —")
        comp_row.addWidget(self.est_label)
        root.addLayout(comp_row)

        est_btn = QPushButton("Estimate Selected")
        est_btn.setToolTip("Estimates compressed size for the first selected file (or top file if none selected).")
        est_btn.clicked.connect(self.estimate_selected)
        root.addWidget(est_btn)

        # Output folder
        out_row = QHBoxLayout()
        pick_out = QPushButton("Choose Output Folder…"); pick_out.clicked.connect(self.choose_output)
        out_row.addWidget(pick_out)
        root.addLayout(out_row)

        # Progress
        self.perfile_bar = QProgressBar(); self.perfile_bar.setFormat("Current file: %p%")
        self.global_bar = QProgressBar(); self.global_bar.setFormat("Overall: %p%")
        self.eta_label = QLabel("ETA: —")
        root.addWidget(self.perfile_bar); root.addWidget(self.global_bar); root.addWidget(self.eta_label)

        start = QPushButton("Start"); start.clicked.connect(self.start_process)
        root.addWidget(start)

        self.setLayout(root)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp)")
        for f in files:
            self.listw.addItem(f)

    def choose_output(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if d:
            self.output_dir = d

    def estimate_selected(self):
        if self.listw.count() == 0:
            QMessageBox.information(self, "No files", "Add images first.")
            return
        items = self.listw.selectedItems()
        path = items[0].text() if items else self.listw.item(0).text()
        est, ratio = estimate_compressed_size(path, fmt=self.fmt.currentText(), quality=self.quality.value())
        if est is None:
            self.est_label.setText("Estimated size: —")
        else:
            kb = max(1, round(est / 1024))
            self.est_label.setText(f"Estimated size: {kb} KB (≈{ratio:.2f}× of original)")

    def start_process(self):
        files = [self.listw.item(i).text() for i in range(self.listw.count())]
        if not files:
            QMessageBox.warning(self, "No files", "Please add images."); return
        size = None
        if self.sizepreset.currentText() != "None":
            size = target_dims_from_preset(self.sizepreset.currentText())
        self.t0 = time.time()
        self.worker = Worker(
            files, self.fmt.currentText(), size, self.keep_aspect.isChecked(),
            self.quality.value(), outdir=self.output_dir
        )
        self.worker.perfile.connect(self.on_perfile)
        self.worker.progress.connect(self.on_progress)
        self.worker.started_file.connect(self.on_started_file)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_started_file(self, path):
        self.perfile_bar.setValue(0)

    def on_perfile(self, pct, _):
        self.perfile_bar.setValue(pct)

    def on_progress(self, pct, _):
        self.global_bar.setValue(pct)
        elapsed = time.time() - self.t0
        if pct > 0:
            total_est = elapsed / (pct / 100.0)
            eta = max(0, int(total_est - elapsed))
            self.eta_label.setText(f"ETA: {eta}s")

    def on_finished(self):
        self.perfile_bar.setValue(100)
        self.eta_label.setText("ETA: 0s — Done")
        QMessageBox.information(self, "Done", "All images processed.")
