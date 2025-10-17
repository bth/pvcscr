import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

class PvcScr(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("PvcScr")

def main():
    print("pvcscr")
    app = QApplication(sys.argv)
    #label = QLabel("Hello World", alignment=Qt.Alignment.AlignCenter)
    #label.show()
    window = PvcScr()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
