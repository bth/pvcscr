import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

class PvcScr(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("PvcScr")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

def main():
    print("pvcscr")
    app = QApplication(sys.argv)
    window = PvcScr()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
