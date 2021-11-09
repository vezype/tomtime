# -*- coding: utf-8 -*-
# Автор: Дмитрий Гиль.

import sys

from datetime import datetime

from loader import db, ntf

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('interface/window.ui', self)
        self.setFixedSize(1080, 720)

        self.group_boxes = {
            self.btn_all: self.gb_all_tasks,
            self.btn_today: self.gb_today_tasks,
            self.btn_overdue: self.gb_overdue_tasks,
            self.btn_completed: self.gb_completed_tasks,
            'Начальная заставка': self.gb_screensaver
        }
        [group_box.hide() for group_box in list(self.group_boxes.values())[:-1]]
        [btn.clicked.connect(self.group_box_show) for btn in list(self.group_boxes.keys())[:-1]]

        current_time = datetime.now()
        self.current_day = current_time.strftime('%Y-%m-%d')
        self.task_date.setMinimumDate(QDate(current_time.year, current_time.month, current_time.day))

    def group_box_show(self) -> None:
        self.group_boxes[self.sender()].show()
        for btn in self.group_boxes.keys():
            if btn != self.sender():
                self.group_boxes[btn].hide()

    def update_table_all_tasks(self) -> None:
        self.table_all_tasks.setRowCount(0)
        result = db.get_all_tasks(sort_key=self.sort_box.currentText())

        for e, row in enumerate(result):
            self.table_all_tasks.setRowCount(self.table_all_tasks.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_all_tasks.setItem(e, j, QTableWidgetItem(str(elem)))

    def update_table_completed_tasks(self) -> None:
        self.table_completed_tasks.setRowCount(0)
        result = db.get_completed_tasks(sort_key=self.sort_box.currentText())

        for e, row in enumerate(result):
            self.table_completed_tasks.setRowCount(self.table_completed_tasks.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_completed_tasks.setItem(e, j, QTableWidgetItem(str(elem)))

    def update_table_overdue_tasks(self) -> None:
        self.table_overdue_tasks.setRowCount(0)
        result = db.get_overdue_tasks(sort_key=self.sort_box.currentText(), current_day=self.current_day)

        for e, row in enumerate(result):
            self.table_overdue_tasks.setRowCount(self.table_overdue_tasks.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_overdue_tasks.setItem(e, j, QTableWidgetItem(str(elem)))

    def update_table_today_tasks(self) -> None:
        self.table_today_tasks.setRowCount(0)
        result = db.get_today_tasks(sort_key=self.sort_box.currentText(), current_day=self.current_day)

        for e, row in enumerate(result):
            self.table_today_tasks.setRowCount(self.table_today_tasks.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_today_tasks.setItem(e, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        del db


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
