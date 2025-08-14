import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from home_tab import HomeTab
from image_tools_tab import ImageToolsTab
from file_tools_tab import FileToolsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utility Tool")
        self.setGeometry(200, 200, 1000, 700)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        tabs = QTabWidget()
        tabs.addTab(HomeTab(), "Home")
        tabs.addTab(ImageToolsTab(), "Image Tools")
        tabs.addTab(FileToolsTab(), "File Tools")

        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
