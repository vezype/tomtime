# -*- coding: utf-8 -*-
# Автор: Дмитрий Гиль.

import sys

from datetime import datetime

from loader import db, ntf

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QTableWidgetItem


class TransferTaskForm(QWidget):
    def __init__(self, task_id: int, date_object: QDate, current_day: str, update_functions: list):
        super(TransferTaskForm, self).__init__()
        uic.loadUi('interface/transfer_task.ui', self)
        self.setFixedSize(330, 95)

        self.new_time_task.setMinimumDate(date_object)
        self.update_funcs, self.id, self.current_day = update_functions, task_id, current_day

        self.btn_save.clicked.connect(self.save)

    def save(self) -> None:
        date, time = self.new_time_task.date(), self.new_time_task.time()
        date = f'{date.year()}-{date.month()}-{date.day()} {time.hour()}:' \
               f'{"0" + str(time.minute()) if time.minute() < 10 else time.minute()}'

        db.update_date_task(self.id, date)

        if self.current_day < date.split()[0]:
            for update_function in self.update_funcs[:-1]:
                update_function()
        else:
            for update_function in self.update_funcs:
                update_function()

        self.hide()


class EditTaskForm(QWidget):
    def __init__(self, task_id: int, update_functions: list):
        super(EditTaskForm, self).__init__()
        uic.loadUi('interface/edit_task.ui', self)
        self.setFixedSize(460, 185)

        self.update_functions = update_functions
        self.task_id = task_id
        self.title, self.description, self.date, self.tag_id, self.priority_id = db.get_task(self.task_id)
        self.tag, self.priority = db.get_tag_title(self.tag_id), db.get_priority_title(self.priority_id)

        self.task_name.setPlainText(self.title)
        self.task_description.setPlainText(self.description)
        year, month, day = self.date.split()[0].split('-')
        hour, minute = self.date.split()[-1].split(':')
        time_object = QTime(int(hour), int(minute))
        date_object = QDate(int(year), int(month), int(day))
        self.task_date.setDate(date_object)
        self.task_date.setTime(time_object)
        self.set_tag.addItems(db.get_title_tags())
        self.set_priority.setCurrentText(self.priority)
        self.set_tag.setCurrentText(self.tag)

        self.btn_save.clicked.connect(self.save)

    def save(self) -> None:
        if self.task_name.toPlainText():
            tag_id = db.get_tag_id(self.set_tag.currentText())
            priority_id = db.get_priority_id(self.set_priority.currentText())
            date, time = self.task_date.date(), self.task_date.time()
            date = f'{date.year()}-{date.month()}-{date.day()} {time.hour()}:' \
                   f'{"0" + str(time.minute()) if time.minute() < 10 else time.minute()}'

            db.update_task(self.task_id, self.task_name.toPlainText(), self.task_description.toPlainText(),
                           date, tag_id, priority_id)

            for update_function in self.update_functions:
                update_function()

            self.hide()


class EditTodayTaskForm(QWidget):
    def __init__(self, task_id: int, update_functions: list):
        super(EditTodayTaskForm, self).__init__()
        uic.loadUi('interface/edit_task_today.ui', self)
        self.setFixedSize(460, 185)

        self.update_functions = update_functions
        self.task_id = task_id
        self.title, self.description, self.date, self.tag_id, self.priority_id = db.get_task(self.task_id)
        self.tag, self.priority = db.get_tag_title(self.tag_id), db.get_priority_title(self.priority_id)

        self.task_name.setPlainText(self.title)
        self.task_description.setPlainText(self.description)
        year, month, day = self.date.split()[0].split('-')
        hour, minute = self.date.split()[-1].split(':')
        time_object = QTime(int(hour), int(minute))
        date_object = QDate(int(year), int(month), int(day))
        self.task_date_2.setDate(date_object)
        self.task_date_2.setTime(time_object)
        self.set_tag.addItems(db.get_title_tags())
        self.set_priority.setCurrentText(self.priority)
        self.set_tag.setCurrentText(self.tag)

        self.btn_save.clicked.connect(self.save)

    def save(self) -> None:
        if self.task_name.toPlainText():
            tag_id = db.get_tag_id(self.set_tag.currentText())
            priority_id = db.get_priority_id(self.set_priority.currentText())
            date, time = self.task_date_2.date(), self.task_date_2.time()
            date = f'{date.year()}-{date.month()}-{date.day()} {time.hour()}:' \
                   f'{"0" + str(time.minute()) if time.minute() < 10 else time.minute()}'

            db.update_task(self.task_id, self.task_name.toPlainText(), self.task_description.toPlainText(),
                           date, tag_id, priority_id)

            for update_function in self.update_functions:
                update_function()

            self.hide()


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
        for group_box in list(self.group_boxes.values())[:-1]:
            group_box.hide()
        for btn in list(self.group_boxes.keys())[:-1]:
            btn.clicked.connect(self.group_box_show)

        current_time = datetime.now()
        self.current_day = current_time.strftime('%Y-%m-%d')
        self.date_object = QDate(current_time.year, current_time.month, current_time.day)
        self.task_date.setMinimumDate(self.date_object)

        self.buttons_and_tables = {
            self.btn_del_task: (self.table_all_tasks, self.update_table_all_tasks),
            self.btn_del_task_2: (self.table_today_tasks, self.update_table_today_tasks),
            self.btn_del_task_3: (self.table_completed_tasks, self.update_table_completed_tasks),
            self.btn_del_task_4: (self.table_overdue_tasks, self.update_table_overdue_tasks),
            self.btn_complete_task: (self.table_all_tasks, self.update_table_all_tasks),
            self.btn_complete_task_2: (self.table_today_tasks, self.update_table_today_tasks),
            self.btn_complete_task_3: (self.table_overdue_tasks, self.update_table_overdue_tasks)
        }
        for btn, update_func in list(self.buttons_and_tables.items())[:4]:
            btn.clicked.connect(self.del_task)
            update_func[-1]()
        for btn in list(self.buttons_and_tables.keys())[4:]:
            btn.clicked.connect(self.complete_task)

        self.btn_add_task.clicked.connect(self.add_task)
        self.btn_add_task_2.clicked.connect(self.add_today_task)
        self.btn_transfer_task.clicked.connect(self.transfer_task)
        self.btn_edit_task.clicked.connect(self.edit_task)
        self.btn_edit_task_2.clicked.connect(self.edit_today_task)

    def group_box_show(self) -> None:
        self.group_boxes[self.sender()].show()
        for btn in self.group_boxes.keys():
            if btn != self.sender():
                self.group_boxes[btn].hide()

    def edit_task(self) -> None:
        selected_items = self.table_all_tasks.selectedItems()

        if selected_items:
            item = selected_items[0]
            task_id = int(self.table_all_tasks.item(item.row(), 0).text())

            self.edit_task_form = EditTaskForm(task_id, [self.update_table_all_tasks, self.update_table_today_tasks])
            self.edit_task_form.show()

    def edit_today_task(self) -> None:
        selected_items = self.table_today_tasks.selectedItems()

        if selected_items:
            item = selected_items[0]
            task_id = int(self.table_today_tasks.item(item.row(), 0).text())

            self.edit_task_today_form = EditTodayTaskForm(task_id,
                                                          [self.update_table_all_tasks, self.update_table_today_tasks])
            self.edit_task_today_form.show()

    def transfer_task(self) -> None:
        selected_items = self.table_overdue_tasks.selectedItems()

        if selected_items:
            item = selected_items[0]
            task_id = int(self.table_overdue_tasks.item(item.row(), 0).text())

            self.transfer_task_form = TransferTaskForm(task_id, self.date_object, self.current_day,
                                                       [self.update_table_all_tasks, self.update_table_overdue_tasks,
                                                        self.update_table_today_tasks])
            self.transfer_task_form.show()

    def add_task(self) -> None:
        title = self.task_name.toPlainText()
        description = self.task_description.toPlainText()
        date, time = self.task_date.date(), self.task_date.time()
        date = f'{date.year()}-{date.month()}-{date.day()} {time.hour()}:' \
               f'{"0" + str(time.minute()) if time.minute() < 10 else time.minute()}'
        priority = db.get_priority_id(self.set_priority.currentText())
        tag = db.get_tag_id(self.set_tag.currentText())
        if title:
            db.add_task(title, description, date, tag, priority)
            self.update_table_all_tasks()
            if self.current_day == date.split()[0]:
                self.update_table_today_tasks()

    def add_today_task(self) -> None:
        title = self.task_name_2.toPlainText()
        description = self.task_description_2.toPlainText()
        time = self.task_date_2.time()
        date = f'{self.current_day} {time.hour()}:{"0" + str(time.minute()) if time.minute() < 10 else time.minute()}'
        priority = db.get_priority_id(self.set_priority_2.currentText())
        tag = db.get_tag_id(self.set_tag_2.currentText())
        if title:
            db.add_task(title, description, date, tag, priority)
            self.update_table_all_tasks()
            self.update_table_today_tasks()

    def del_task(self) -> None:
        table, update_func = self.buttons_and_tables[self.sender()]
        selected_items = table.selectedItems()

        if selected_items:
            item = selected_items[0]
            task_id = int(table.item(item.row(), 0).text())
            if table == self.table_completed_tasks:
                db.del_completed_task(task_id)
            else:
                db.del_task(task_id)
            update_func()

    def complete_task(self) -> None:
        table, update_func = self.buttons_and_tables[self.sender()]
        selected_items = table.selectedItems()

        if selected_items:
            item = selected_items[0]
            task_id = int(table.item(item.row(), 0).text())
            db.mark_task_completed(task_id)
            update_func()
            self.update_table_completed_tasks()

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
        db.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
