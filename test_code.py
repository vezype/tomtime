# -*- coding: utf-8 -*-
# Автор: Дмитрий Гиль.

from PyQt5.QtCore import QTimer
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QLabel


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 250, 330, 60)
        self.setWindowTitle('Вычисление выражений')

        self.timer = QTimer(self)
        self.timer.start(1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
