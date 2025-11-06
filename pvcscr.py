import sys
from PySide6.QtCore import Qt, QRect, QPoint, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QStyle
from PySide6.QtGui import QRegion, QCursor

class PvcScr(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PvcScr")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.frame = QFrame(self)
        self.frame.setFrameStyle(1)
        self.frame.setStyleSheet("QFrame { background-color: rgba(0, 0, 0, 200); }")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.timer.start(10)
        self.hole = QRect(0, 0, 0, 0)
        self.hole_width = 200
        self.hole_height = 100
        self.title_bar_height = self.style().pixelMetric(QStyle.PM_TitleBarHeight)

    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, event.size().width(), event.size().height())
        self.repaint()

    def positionHole(self, mouse_position):
        self.hole = QRect(mouse_position.x() - self.hole_width/2, mouse_position.y() - self.hole_height/2, self.hole_width, self.hole_height)
        region = QRegion(QRect(QPoint(0, 0), self.size()), QRegion.RegionType.Rectangle)
        empty_region = QRegion(self.hole, QRegion.RegionType.Rectangle)
        os_bar = QRegion(QRect(0, -self.title_bar_height, self.size().width(), self.title_bar_height), QRegion.RegionType.Rectangle)
        self.setMask(region - empty_region + os_bar)

    def time(self):
        global_pos = QCursor.pos()
        local_pos_from_global = self.mapFromGlobal(global_pos)
        self.positionHole(local_pos_from_global)

def main():
    app = QApplication(sys.argv)
    window = PvcScr()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
