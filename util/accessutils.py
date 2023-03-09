from mysql.connector import MySQLConnection, Error

from database.python_mysql_dbconfig import read_db_config


async def getwhohasaccess(user):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"SELECT userid from access where userid=%(userid)s;"
            user_data = {
                'userid': user,
            }
            c.execute(sql, user_data)
            user = c.fetchone()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
            if not user:
                return False
            return user
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e
async def whohasaccess(userid):
    data = await getwhohasaccess(userid)
    return data