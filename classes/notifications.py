from plyer import notification


class Notifications:
    def notify(self, today_tasks: int, overdue_tasks: int) -> None:
        message = f'Задач на сегодня: {today_tasks}\n' \
                  f'Просроченных задач: {overdue_tasks}'

        notification.notify(
            title='Приятного времяпровождения!',
            message=message,
            app_name='Tomtime'
        )
