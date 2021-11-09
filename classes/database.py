import sqlite3


class SQLRequests:
    def __init__(self, way_to_database: str = './db.sqlite'):
        self.connection = sqlite3.connect(way_to_database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def del_task(self, task_id: int) -> None:
        self.cursor.execute(f'DELETE FROM all_tasks WHERE id = {task_id}')
        self.connection.commit()

    def del_completed_task(self, task_id: int) -> None:
        self.cursor.execute(f'DELETE FROM completed_tasks WHERE id = {task_id}')
        self.connection.commit()

    def del_tag(self, tag_id: int) -> None:
        self.cursor.execute(f'DELETE FROM my_tags WHERE id = {tag_id}')
        self.connection.commit()

    def add_tag(self, title: str, color: str) -> None:
        request = 'INSERT INTO my_tags(title, color) VALUES (?, ?)'
        data = (title, color)
        self.cursor.execute(request, data)
        self.connection.commit()

    def add_task(self, title: str, description: str, date: str, tag: int = 0, priority: int = 0) -> None:
        request = 'INSERT INTO all_tasks(title, description, date, tag, priority) VALUES (?, ?, ?, ?, ?)'
        data = (title, description, date, tag, priority)
        self.cursor.execute(request, data)
        self.connection.commit()

    def mark_task_completed(self, task_id: int) -> None:
        request = f'SELECT title, description, date, tag, priority FROM all_tasks WHERE id = {task_id}'
        data = self.cursor.execute(request).fetchone()
        self.del_task(task_id)
        request = 'INSERT INTO completed_tasks(title, description, date, tag, priority) VALUES (?, ?, ?, ?, ?)'
        self.connection.execute(request, data)
        self.connection.commit()

    def update_task(self, id: int, title: str, description: str, date: str, tag: int = 0, priority: int = 0) -> None:
        request = f'''UPDATE all_tasks
        SET title = ?, description = ?, date = ?, tag = ?, priority = ?
        WHERE id = {id}'''
        data = (title, description, date, tag, priority)
        self.cursor.execute(request, data)
        self.connection.commit()

    def get_today_tasks(self, current_day: str, sort_key: str = 'По дате добавления') -> list:
        data = self.cursor.execute('SELECT * FROM all_tasks').fetchall()
        tasks = []
        for task in data:
            if task[3].split()[0] == current_day:
                tasks.append(task)
        if sort_key == 'По дате добавления':
            tasks.sort(key=lambda task: task[3])
        else:
            tasks.sort(key=lambda task: task[-1], reverse=True)
        return tasks

    def get_all_tasks(self, sort_key: str = 'По дате добавления') -> list:
        tasks = self.cursor.execute('SELECT * FROM all_tasks').fetchall()
        if sort_key == 'По дате добавления':
            tasks.sort(key=lambda task: task[3])
        else:
            tasks.sort(key=lambda task: task[-1], reverse=True)
        return tasks

    def get_completed_tasks(self, sort_key: str = 'По дате добавления') -> list:
        tasks = self.cursor.execute('SELECT * FROM completed_tasks').fetchall()
        if sort_key == 'По дате добавления':
            tasks.sort(key=lambda task: task[3])
        else:
            tasks.sort(key=lambda task: task[-1], reverse=True)
        return tasks

    def get_overdue_tasks(self, current_day: str, sort_key: str = 'По дате добавления') -> list:
        data = self.cursor.execute('SELECT * FROM all_tasks').fetchall()
        tasks = []
        for task in data:
            if task[3].split()[0] < current_day:
                tasks.append(task)
        if sort_key == 'По дате добавления':
            tasks.sort(key=lambda task: task[3])
        else:
            tasks.sort(key=lambda task: task[-1], reverse=True)
        return tasks
