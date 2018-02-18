import hashlib
from lib542.sql import *


def generate_session(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()


def generate_user_id():
    statement = 'select UserID from Users order by UserID desc;'
    result = sql_execute(statement)
    return result[0][0] + 1


def create_account(username, password):
    user_id = generate_user_id()
    session = generate_session(password)
    statement = 'INSERT INTO Users VALUES (' + \
                str(user_id) + ',\'' + \
                username + '\',\'' + password + \
                '\',\'' + session + '\');'
    sql_insert(statement)
    return session


def authentication(s_username, s_password):
    statement = 'SELECT password, session FROM Users WHERE username=\'' + s_username + '\''
    result = sql_execute(statement)
    auth_result = []
    if len(result) == 0:
        auth_result.append(False)
        return auth_result
    else:
        password = result[0][0]
        if s_password == password:
            auth_result.append(True)
            auth_result.append(result[0][1])
            return auth_result
        else:
            auth_result.append(False)
            return auth_result


def extract_profile(session):
    statement = "SELECT userid, username FROM Users WHERE session='%s';" % session
    print('---> Executing SQL Statement')
    print(statement)
    result = sql_execute(statement)

    if len(result) == 0:
        return [False]
    else:
        return [True, result[0]]
