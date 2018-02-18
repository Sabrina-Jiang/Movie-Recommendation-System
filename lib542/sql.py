import mysql.connector


# SQL related functions
def sql_execute(statement):
    cnx = mysql.connector.connect(user='root', database='c9')
    c = cnx.cursor()
    c.execute(statement)
    result = []
    for row in c:
        result.append(row)
    cnx.close()
    return result


def sql_insert(statement):
    cnx = mysql.connector.connect(user='root', database='c9')
    c = cnx.cursor()
    c.execute(statement)
    cnx.commit()
    cnx.close()
