# -*- coding: utf-8 -*-
# Автор: Дмитрий Гиль.

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QGroupBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('interface/window.ui', self)
        self.setFixedSize(1080, 720)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
