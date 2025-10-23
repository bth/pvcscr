import sys
from PySide6.QtCore import Qt, QRect, QPoint, QSize, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame
from PySide6.QtGui import QRegion

class PvcScr(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PvcScr")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.move(100, 100)
        self.frame = QFrame(self)
        self.frame.setFrameStyle(1)
        self.frame.setStyleSheet("QFrame { border: 5px solid red;}")
        self.setMouseTracking(True)
        self.frame.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.timer.start(1000)

    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, event.size().width(), event.size().height())

    def mouseMoveEvent(self, event):
        # Position relative à la fenêtre
        local_pos = event.pos()
        print(f"Position locale dans la fenêtre : {local_pos.x()}, {local_pos.y()}")

    def time(self):
        empty_region = QRegion(QRect(QPoint(5,5), self.frame.size() - QSize(10, 10)), QRegion.RegionType.Rectangle)
        region = QRegion(QRect(QPoint(-2,-2), self.frame.size() + QSize(4, 4)), QRegion.RegionType.Rectangle)
        self.setMask(region - empty_region)


def main():
    print("pvcscr")
    app = QApplication(sys.argv)
    window = PvcScr()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
