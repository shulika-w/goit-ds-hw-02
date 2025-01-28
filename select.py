import sqlite3

from random import randint

import faker


def get_user_tasks(user_id):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        tasks = cur.fetchall()
    return tasks


def get_status_tasks(status_id):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE status_id = ?", (status_id,))
        tasks = cur.fetchall()
    return tasks


def update_status_task(new_status_id, task_id):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE tasks SET status_id = ? WHERE id = ?", (new_status_id, task_id))
        tasks = cur.fetchall()
        return tasks


def get_users_without_tasks():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
        users = cur.fetchall()
        return users


def add_task_for_user(title, description, status_id, user_id):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
                    (title, description, status_id, user_id))
        task = cur.fetchall()
        return task


def get_tasks_in_work():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE status_id != 3")
        tasks = cur.fetchall()
        return tasks


def delete_task(task_id):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        task = cur.fetchall()
        return task


def get_users_from_email():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email LIKE '%o%'")
        users = cur.fetchall()
        return users


def update_username(username, id):
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET fullname = ? WHERE id = ?", (username, id))
        username = cur.fetchall()
        return username


def get_tasks_by_status():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) as total_tasks, status_id FROM tasks GROUP BY status_id")
        tasks = cur.fetchall()
        return tasks


def get_tasks_by_domain():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        # cur.execute("SELECT t.title, t.description, u.email FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE '%@example.com%'")
        cur.execute(
            "SELECT t.title, u.email FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE '%@example.com%'")
        tasks = cur.fetchall()
        return tasks


def get_tasks_without_description():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE description IS NULL")
        tasks = cur.fetchall()
        return tasks


def get_users_and_tasks_in_progress():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        cur.execute(
            "SELECT u.fullname, t.title FROM tasks t INNER JOIN users u ON u.id = t.user_id WHERE t.status_id = 2")
        users = cur.fetchall()
        return users


def get_tasks_for_each_user():
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()
        # cur.execute("SELECT u.fullname, t.title FROM tasks t LEFT JOIN users u WHERE (SELECT COUNT(id) as total_tasks FROM tasks GROUP BY user_id)")
        cur.execute(
            "SELECT COUNT(t.id) as total_tasks, u.fullname FROM tasks t LEFT JOIN users u ON t.user_id = u.id GROUP BY user_id")
        tasks = cur.fetchall()
        return tasks


if __name__ == '__main__':
    # 1. Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.

    user_id = randint(1, 10)

    user_tasks = get_user_tasks(user_id)
    print(f"1. Завдання для користувача з id {user_id}: {user_tasks}")

    # 2. Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.

    status_id = randint(1, 3)

    status_tasks = get_status_tasks(status_id)
    print(f"2. Статус '{status_id}' мають такі завдання: {status_tasks}")

    # 3. Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.

    task_id = randint(1, 3)
    new_status_id = randint(1, 3)

    update_status_task(new_status_id, task_id)
    print(f"3. Завдання {task_id} тепер має статус {new_status_id}")

    # 4. Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.

    print(f"4. Завдань не мають такі користувачі: {get_users_without_tasks()}")

    # 5. Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.

    new_task = (("test title"), ("test description"))
    random_user_id = randint(1, 10)

    task = add_task_for_user("test title", "test description", randint(1, 3), random_user_id)

    print(f"5. Завдання {new_task[0]} було закріплено за користувачем з id: {random_user_id}")

    # 6. Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.

    print(f"6. Над такими завданнями ще триває робота:{get_tasks_in_work()}")

    # 7. Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.

    task_id = randint(1, 5)
    delete_task(task_id)

    print(f"7. Завдання з id {task_id} було видалено.")

    # 8. Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.

    users = get_users_from_email()

    print(f"8. Літера 'o' міститься в електронній пошті таких користувачів: {users}")

    # 9. Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.

    id = randint(1, 10)
    fake_username = faker.Faker()
    new_username = fake_username.name()

    update_username(new_username, id)

    print(f"9. Імʼя користувача з id {id} змінено на: {new_username}")

    # 10. Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.

    grouped_tasks = get_tasks_by_status()

    print(
        f"10. Кількість завдань зі статусами: 'new' – {grouped_tasks[0][0]}, 'in progress' – {grouped_tasks[1][0]}, 'completed' – {grouped_tasks[2][0]}.")

    # 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').

    print(f"11. Список завдань користувачів з доменом '@example.com': {get_tasks_by_domain()}")

    # 12. Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.

    print(f"12. Опису не мають такі завдання: {get_tasks_without_description()}.")

    # 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.

    print(f"13. Список користувачів та завдань зі статусом 'in progress': {get_users_and_tasks_in_progress()}")

    # 14. Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.

    users_with_tasks = get_tasks_for_each_user()

    print(f"14. Список користувачів з кількістю закріпленими за ними завдань: {users_with_tasks}.")
