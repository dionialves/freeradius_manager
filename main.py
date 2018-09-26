import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from views.mainwindow import MainWindow


def main():
    application = QApplication(sys.argv)
    window = MainWindow()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
