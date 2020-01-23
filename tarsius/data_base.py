# -*- coding: utf-8
import pymysql
#import mysql.connector


def connect_to_db():
    print('trying to connect...')
    connection = pymysql.connect(
        host='79.111.246.189',
        port=3306,
        user='pi',
        password='matrega',
        db='tarsius',
        charset='utf8',
    )
    print(connection, connection.host_info)
    return connection


def create_new_worker(user_id, user_username, chat_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM project1")
    respond = ''
    myresult = cursor.fetchall()
    username_list = []
    for x in myresult:
        username_list.append(x[0])
        print(username_list)
    if user_username in username_list:
        respond = 'yes'
    else:
        respond = 'no'
    cursor.close()
    connection.close()
    print('Respond is: {}\nConnection closed'.format(respond))
    return respond


def get_details_for_task(user_username):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT name, project_name, task, deadline, link_to_TZ FROM project1 WHERE username=%s", user_username)
    myresult = cursor.fetchone()
    print(myresult)
    #return name, project_name, task, deadline, link_to_TZ
    name = myresult[0]
    project_name = myresult[1]
    task = myresult[2]
    deadline = myresult[3]
    link_to_TZ = myresult[4]
    cursor.close()
    connection.close()
    return name, project_name, task, deadline, link_to_TZ


def save_comment_from_user(user_username, text):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "UPDATE project1 SET comment='{}' WHERE username='{}'".format(text, user_username)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


def get_status():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT name, soname, project_name, deadline, comment FROM project1")
    myresult = cursor.fetchall()
    status_list = []
    for x in myresult:
        status = '{} {}\nПроект "{}"\nДедлайн: {}\n Статус "{}"'.format(x[0], x[1], x[2], x[3], x[4])
        status_list.append(status)
        print(status)
    total_status = '\n\n'.join(status_list)
    return total_status