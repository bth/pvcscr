import subprocess
import sys, os, configparser
from PySide6.QtCore import Qt, QRect, QPoint, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QHBoxLayout, QLabel, QSizeGrip
from PySide6.QtGui import QRegion, QCursor, QResizeEvent

try:
    from version import VERSION
except:
    VERSION = "dev"

class PvcScr(QMainWindow):

    BUTTON_SIZE = 20
    BUTTON_SPACE = 5
    NUMBER_OF_BUTTONS = 6

    def __init__(self):
        super().__init__()
        print(f"{VERSION}")
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

        self.bar = QFrame(self)
        self.bar_width = self.NUMBER_OF_BUTTONS * (self.BUTTON_SIZE + self.BUTTON_SPACE)
        self.bar_height = self.BUTTON_SIZE + (self.BUTTON_SPACE * 2)
        self.bar_position = Qt.AlignRight

        self.buttons_layout = QHBoxLayout(self.bar)
        self.buttons_layout.setContentsMargins(self.BUTTON_SPACE, 0, self.BUTTON_SPACE, 0)

        self.move_label = QLabel("✥")
        self.move_label.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.move_label.setToolTip("Move window")
        self.move_label.setAlignment(Qt.AlignCenter)
        self.move_label.setStyleSheet("QLabel { background-color: white;}")
        self.buttons_layout.addWidget(self.move_label)

        button = QPushButton("↔")
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.setToolTip("Move buttons")
        button.clicked.connect(self.toggleBarPosition)
        self.buttons_layout.addWidget(button)

        button = QPushButton("⚙️")
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.setToolTip("Edit configuration")
        button.clicked.connect(self.openConfiguration)
        self.buttons_layout.addWidget(button)

        button = QPushButton("—")
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.clicked.connect(self.showMinimized)
        self.buttons_layout.addWidget(button)

        button = QPushButton("□")
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.clicked.connect(self.toggleFullScreen)
        self.buttons_layout.addWidget(button)

        button = QPushButton("✕")
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.clicked.connect(self.close)
        self.buttons_layout.addWidget(button)

        self.grip_tl = QSizeGrip(self)
        self.grip_tl.resize(self.BUTTON_SPACE, self.BUTTON_SPACE)

        self.grip_tr = QSizeGrip(self)
        self.grip_tr.resize(self.BUTTON_SPACE, self.BUTTON_SPACE)

        self.grip_bl = QSizeGrip(self)
        self.grip_bl.resize(self.BUTTON_SPACE, self.BUTTON_SPACE)
        
        self.grip_br = QSizeGrip(self)
        self.grip_br.resize(self.BUTTON_SPACE, self.BUTTON_SPACE)

    def toggleBarPosition(self):
        self.bar_position = Qt.AlignLeft if self.bar_position == Qt.AlignRight else Qt.AlignRight
        self.resizeEvent(QResizeEvent(self.size(), self.size()))

    def openConfiguration(self):
        if sys.platform == "win32":
            subprocess.run(["start", self.config_file], shell=True)
        else:
            subprocess.run(["xdg-open", self.config_file])

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
        self.config_file = os.path.join(user_path, 'pvcscr.cfg')
        config = configparser.ConfigParser()

        if not os.path.exists(self.config_file):
            config['DEFAULT'] = {
                'check_mouse_poll': DEFAULT_CHECK_MOUSE_POLL,
                'hole_width': DEFAULT_HOLE_WIDTH,
                'hole_height': DEFAULT_HOLE_HEIGHT,
                'opacity': DEFAULT_OPACITY
            }
            with open(self.config_file, "w") as f:
                f.write("# Configuration changes require a restart of the application to take effect.\n")
                config.write(f)
        
        config.read(self.config_file)
        self.check_mouse_poll = config.getint('DEFAULT', 'check_mouse_poll', fallback=DEFAULT_CHECK_MOUSE_POLL)
        self.hole_width = config.getint('DEFAULT', 'hole_width', fallback=DEFAULT_HOLE_WIDTH)
        self.hole_height = config.getint('DEFAULT', 'hole_height', fallback=DEFAULT_HOLE_HEIGHT)
        self.opacity = config.getfloat('DEFAULT', 'opacity', fallback=DEFAULT_OPACITY)

    def positionGrips(self):
        self.grip_tl.move(0, 0)
        self.grip_tr.move(self.frame.width() - self.BUTTON_SPACE, 0)
        self.grip_bl.move(0, self.frame.height() - self.BUTTON_SPACE)
        self.grip_br.move(self.frame.width() - self.BUTTON_SPACE, self.frame.height() - self.BUTTON_SPACE)

    def resizeEvent(self, event):
        self.frame.setGeometry(0, 0, event.size().width(), event.size().height())
        bar_x = 0
        if self.bar_position == Qt.AlignRight:
            bar_x = event.size().width() - self.bar_width
        self.bar.setGeometry(bar_x, 0, self.bar_width, self.bar_height)
        self.positionGrips()

    def positionHole(self, mouse_position):
        self.hole = QRect(mouse_position.x() - self.hole_width/2, mouse_position.y() - self.hole_height/2, self.hole_width, self.hole_height)
        window_region = QRegion(QRect(QPoint(0, 0), self.size()), QRegion.RegionType.Rectangle)
        empty_region = QRegion(self.hole, QRegion.RegionType.Rectangle)
        bar_region = QRegion(self.bar.geometry());
        grips_region = QRegion()
        if not self.isFullScreen() :
            grips_region = QRegion(self.grip_tl.geometry()) + QRegion(self.grip_tr.geometry()) + QRegion(self.grip_bl.geometry()) + QRegion(self.grip_br.geometry())
        self.setMask(window_region - empty_region + bar_region + grips_region)

    def time(self):
        global_pos = QCursor.pos()
        local_pos_from_global = self.mapFromGlobal(global_pos)
        self.positionHole(local_pos_from_global)

    def mouseMoveEvent(self, event):
        position_of_label_in_window = self.move_label.mapTo(self, QPoint(self.move_label.width()/2, self.move_label.height()/2))
        position_of_mouse = event.globalPosition()
        self.move(position_of_mouse.toPoint() - position_of_label_in_window)

def main():
    app = QApplication(sys.argv)
    window = PvcScr()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
