from mysql.connector import MySQLConnection, Error

from database.python_mysql_dbconfig import read_db_config


async def dbget(serverid, bot, valuetoget):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()
            sql = f"SELECT {valuetoget} from {bot} where serverid=%(serverid)s;"
            user_data = {
                'serverid': serverid,
            }
            c.execute(sql, user_data)
            response = c.fetchone()
            if not response:
                return None
            c.close()
            conn.close()
            return response
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


async def dbset(serverid, bot, valuetoset, value):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"UPDATE {bot} SET {valuetoset} = {value} where serverid=%(serverid)s;"
            user_data = {
                'value': value,
                'serverid': serverid,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e
