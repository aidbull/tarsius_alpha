# -*- coding: utf-8
import pymysql

button_help = 'Помощь'


def get_discription(code):
    print('trying to connect')
    connection = pymysql.connect(
        host='79.111.246.189',
        port=3306,
        user='pi',
        password='matrega',
        db='excel',
        charset='utf8',
    )
    print(connection.host_info)
    cursor = connection.cursor()
    send_code = str(code)
    print(send_code)

    cursor.execute("SELECT discription FROM excel WHERE code = %s", send_code)
    version = cursor.fetchone()
    print("Database version: {}".format(version[0]))

    # request = cursor.execute("SELECT discription FROM `excel` WHERE code = %s;", send_code)
    # print(request[0])
    # discript = cursor.fetchone()
    # respond = str(discript[0])
    # print(respond)
    cursor.close()
    connection.close()
    return respond
