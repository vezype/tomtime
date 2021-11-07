# -*- coding: utf-8 -*-
# Автор: Дмитрий Гиль.

import sys, time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QGroupBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('interface/window.ui', self)
        self.setFixedSize(1080, 720)

        self.group_boxes = {
            self.btn_all: self.gb_all_tasks,
            self.btn_today: None,
            self.btn_upcoming: None,
            self.btn_overdue: None,
            self.btn_completed: None,
            'Начальная заставка': None  # Показываем этот group box при запуске приложения.
        }
        # [group_box.hide() for group_box in list(self.group_boxes.values())]
        [btn.clicked.connect(self.group_box_show) for btn in list(self.group_boxes.keys())[:-1]]
        # self.group_boxes['Начальная заставка'].show()

    def group_box_show(self) -> None:
        self.group_boxes[self.sender()].show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
