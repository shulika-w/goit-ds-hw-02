from random import randint, choice

import faker

import sqlite3

NUMBER_USERS = 10
NUMBER_TASKS = 5

STATUS = [('new'), ('in progress'), ('completed')]


def generate_fake_data(number_users, number_tasks) -> tuple():
    fake_usernames = []
    fake_emails = []
    fake_tasks = []
    fake_descriptions = []

    fake_data = faker.Faker()

    for _ in range(number_users):
        fake_usernames.append(fake_data.name())

    for _ in range(number_users):
        fake_emails.append(fake_data.email())

    for _ in range(number_tasks):
        fake_tasks.append(fake_data.text(max_nb_chars=20))

    for _ in range(number_tasks):
        fake_descriptions.append(fake_data.text(max_nb_chars=100))

    return fake_usernames, fake_emails, fake_tasks, fake_descriptions


def prepare_data(usernames, emails, tasks, descriptions, stats) -> tuple():
    for_users = []
    for i in range(len(usernames)):
        for_users.append((usernames[i], emails[i]))

    for_tasks = []
    for i in range(len(tasks)):
        status_id = STATUS.index(choice(STATUS)) + 1
        for_tasks.append((tasks[i], descriptions[i], status_id, randint(1, NUMBER_USERS)))

    for_status = [(i + 1, STATUS[i]) for i in range(len(STATUS))]

    return for_users, for_tasks, for_status


def insert_data_to_db(users, tasks, status) -> None:
    with sqlite3.connect('salary.db') as con:
        cur = con.cursor()

        sql_to_users = """INSERT INTO users(fullname, email) VALUES(?, ?)"""
        cur.executemany(sql_to_users, users)

        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id) VALUES(?, ?, ?, ?)"""
        cur.executemany(sql_to_tasks, tasks)

        sql_to_status = """INSERT INTO status(id, name) VALUES(?, ?)"""
        cur.executemany(sql_to_status, status)

        con.commit()


if __name__ == '__main__':
    users, tasks, status = prepare_data(*generate_fake_data(NUMBER_USERS, NUMBER_TASKS), STATUS)
    insert_data_to_db(users, tasks, status)
