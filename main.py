import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore, QtWidgets
from home_tab import HomeTab
from image_tools_tab import ImageToolsTab
from file_tools_tab import FileToolsTab


def apply_dark(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(235, 235, 235))
    palette.setColor(QPalette.Base, QColor(20, 20, 20))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(235, 235, 235))
    palette.setColor(QPalette.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ButtonText, QColor(235, 235, 235))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

# --- macOS-specific fix for missing Qt 'cocoa' plugin ---
if sys.platform == "darwin":
    plugin_path = os.path.join(os.path.dirname(QtCore.__file__), 'Qt', 'plugins')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utility Tool")
        self.resize(1100, 720)

        tabs = QTabWidget()
        tabs.addTab(HomeTab(), "Home")
        tabs.addTab(ImageToolsTab(), "Image Tools")
        tabs.addTab(FileToolsTab(), "File Tools")

        c = QWidget(); lay = QVBoxLayout(); lay.addWidget(tabs); c.setLayout(lay)
        self.setCentralWidget(c)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark(app)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
