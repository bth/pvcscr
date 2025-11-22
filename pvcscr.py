import sys, os, configparser
from PySide6.QtCore import Qt, QRect, QPoint, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QStyle, QBoxLayout, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSpacerItem, QSizePolicy
from PySide6.QtGui import QRegion, QCursor

class PvcScr(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initConfigFile()
        self.setWindowTitle("PvcScr")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        #self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.frame = QFrame(self)
        self.frame.setFrameStyle(1)
        self.frame.setStyleSheet(f"QFrame {{ background-color: rgba(0, 0, 0, {self.opacity}); }}")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
        self.timer.start(self.check_mouse_poll)
        self.hole = QRect(0, 0, 0, 0)
        self.title_bar_height = 30

        self.bar = QFrame(self)

        self.buttons_layout = QHBoxLayout(self.bar)
        self.buttons_layout.setContentsMargins(5, 0, 5, 0)
        #self.buttons_layout.addStretch()
        self.left_stretch = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttons_layout.addSpacerItem(self.left_stretch)

        self.move_label = QLabel("✥")
        self.move_label.setFixedSize(20, 20)
        self.move_label.setToolTip("Move window")
        self.move_label.setAlignment(Qt.AlignCenter)
        self.move_label.setStyleSheet("QLabel { background-color: white;}")
        self.buttons_layout.addWidget(self.move_label)

        button = QPushButton("↔")
        button.setFixedSize(20, 20)
        button.clicked.connect(self.toggleBarPosition)
        self.buttons_layout.addWidget(button)

        button = QPushButton("—")
        button.setFixedSize(20, 20)
        button.clicked.connect(self.showMinimized)
        self.buttons_layout.addWidget(button)

        button = QPushButton("□")
        button.setFixedSize(20, 20)
        button.clicked.connect(self.toggleFullScreen)
        self.buttons_layout.addWidget(button)

        button = QPushButton("✕")
        button.setFixedSize(20, 20)
        button.clicked.connect(self.close)
        self.buttons_layout.addWidget(button)

    def toggleBarPosition(self):
        pass

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def initConfigFile(self):
        DEFAULT_CHECK_MOUSE_POLL = 10
        DEFAULT_HOLE_WIDTH = 200
        DEFAULT_HOLE_HEIGHT = 100
        DEFAULT_OPACITY = 0.5
        user_path = os.path.join(os.path.expanduser("~"), ".pvcscr")
        os.makedirs(user_path, exist_ok=True)
        config_file = os.path.join(user_path, 'pvcscr.cfg')
        config = configparser.ConfigParser()

        if not os.path.exists(config_file):
            config['DEFAULT'] = {
                'check_mouse_poll': DEFAULT_CHECK_MOUSE_POLL,
                'hole_width': DEFAULT_HOLE_WIDTH,
                'hole_height': DEFAULT_HOLE_HEIGHT,
                'opacity': DEFAULT_OPACITY
            }
            with open(config_file, "w") as f:
                config.write(f)
        
        config.read(config_file)
        self.check_mouse_poll = config.getint('DEFAULT', 'check_mouse_poll', fallback=DEFAULT_CHECK_MOUSE_POLL)
        self.hole_width = config.getint('DEFAULT', 'hole_width', fallback=DEFAULT_HOLE_WIDTH)
        self.hole_height = config.getint('DEFAULT', 'hole_height', fallback=DEFAULT_HOLE_HEIGHT)
        self.opacity = config.getfloat('DEFAULT', 'opacity', fallback=DEFAULT_OPACITY)

    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, event.size().width(), event.size().height())
        self.bar.setGeometry(0, 0, event.size().width(), self.title_bar_height)
        self.repaint()

    def positionHole(self, mouse_position):
        self.hole = QRect(mouse_position.x() - self.hole_width/2, mouse_position.y() - self.hole_height/2, self.hole_width, self.hole_height)
        window_region = QRegion(QRect(QPoint(0, 0), self.size()), QRegion.RegionType.Rectangle)
        empty_region = QRegion(self.hole, QRegion.RegionType.Rectangle)
        bar_region = QRegion(QRect(0, 0, self.size().width(), self.title_bar_height), QRegion.RegionType.Rectangle)
        self.setMask(window_region - empty_region + bar_region)

    def time(self):
        global_pos = QCursor.pos()
        local_pos_from_global = self.mapFromGlobal(global_pos)
        self.positionHole(local_pos_from_global)

    def mouseMoveEvent(self, event):
        position_of_label_in_window = self.move_label.mapTo(self, QPoint(self.move_label.width()/2, self.move_label.height()/2))
        position_of_mouse = event.globalPosition()
        #if self.move_label.geometry().contains(event.position().toPoint()):
        self.move(position_of_mouse.toPoint() - position_of_label_in_window)

def main():
    app = QApplication(sys.argv)
    window = PvcScr()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
