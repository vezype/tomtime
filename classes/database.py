import sqlite3


class SQLRequests:
    def __init__(self, way_to_database: str = './db.sqlite'):
        self.connection = sqlite3.connect(way_to_database)
        self.cursor = self.connection.cursor()

    def del_task(self, task_id: int) -> None:
        self.cursor.execute(f'DELETE FROM all_tasks WHERE id = {task_id}')
        self.connection.commit()

    def del_completed_task(self, task_id: int) -> None:
        self.cursor.execute(f'DELETE FROM completed_tasks WHERE id = {task_id}')
        self.connection.commit()

    def del_tag(self, tag_id: int) -> None:
        self.cursor.execute(f'DELETE FROM my_tags WHERE id = {tag_id}')
        self.cursor.execute(f'UPDATE all_tasks SET tag = 0 WHERE tag = {tag_id}')
        self.connection.commit()

    def add_tag(self, title: str) -> None:
        request = 'INSERT INTO my_tags(title) VALUES (?)'
        data = (title,)
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

    def update_date_task(self, id: int, date: str) -> None:
        request = f'''UPDATE all_tasks
                SET date = '{date}'
                WHERE id = {id}'''
        self.cursor.execute(request)
        self.connection.commit()

    def get_all_tasks(self, sort_key: str = 'По дате добавления') -> list:
        request = '''
        SELECT 
            all_tasks.id, 
            all_tasks.title, 
            all_tasks.description,
            all_tasks.date, 
            my_tags.title, 
            priorities.title,
            all_tasks.priority
        FROM all_tasks
        INNER JOIN my_tags ON all_tasks.tag = my_tags.id
        INNER JOIN priorities ON all_tasks.priority = priorities.id'''
        tasks = self.cursor.execute(request).fetchall()
        if sort_key == 'По дате добавления':
            tasks.sort(key=lambda task: task[3])
        else:
            tasks.sort(key=lambda task: task[-1], reverse=True)
        return [task[:-1] for task in tasks]

    def get_today_tasks(self, current_day: str, sort_key: str = 'По дате добавления') -> list:
        data = self.get_all_tasks(sort_key=sort_key)
        tasks = []
        for task in data:
            if task[3].split()[0] == current_day:
                tasks.append(task)
        return tasks

    def get_completed_tasks(self, sort_key: str = 'По дате добавления') -> list:
        request = '''
        SELECT 
            completed_tasks.id, 
            completed_tasks.title, 
            completed_tasks.description,
            completed_tasks.date, 
            my_tags.title, 
            priorities.title,
            completed_tasks.priority
        FROM completed_tasks
        INNER JOIN my_tags ON completed_tasks.tag = my_tags.id
        INNER JOIN priorities ON completed_tasks.priority = priorities.id'''
        tasks = self.cursor.execute(request).fetchall()
        if sort_key == 'По дате добавления':
            tasks.sort(key=lambda task: task[3])
        else:
            tasks.sort(key=lambda task: task[-1], reverse=True)
        return tasks

    def get_overdue_tasks(self, current_day: str, sort_key: str = 'По дате добавления') -> list:
        data = self.get_all_tasks(sort_key=sort_key)
        tasks = []
        for task in data:
            if task[3].split()[0] < current_day:
                tasks.append(task)
        return tasks

    def get_priority_id(self, title: str) -> int:
        return self.cursor.execute(f'SELECT id FROM priorities WHERE title = "{title}"').fetchone()[0]

    def get_tag_id(self, title: str) -> int:
        return self.cursor.execute(f'SELECT id FROM my_tags WHERE title = "{title}"').fetchone()[0]

    def get_priority_title(self, id: int) -> str:
        return self.cursor.execute(f'SELECT title FROM priorities WHERE id = {id}').fetchone()[0]

    def get_tag_title(self, id: int) -> str:
        return self.cursor.execute(f'SELECT title FROM my_tags WHERE id = {id}').fetchone()[0]

    def get_title_tags(self) -> list:
        return [tag[0] for tag in self.cursor.execute('SELECT title FROM my_tags').fetchall()[1:]]

    def get_task(self, id: int) -> list:
        return list(self.cursor.execute('SELECT title, description, date, tag, priority FROM all_tasks WHERE id = ?',
                                        (id,)).fetchone())

    def get_tags(self) -> list:
        return self.cursor.execute('SELECT * FROM my_tags').fetchall()[1:]
