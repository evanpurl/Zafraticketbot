from mysql.connector import MySQLConnection, Error

from database.python_mysql_dbconfig import read_db_config


async def dbgetlogchannel(categoryname):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()
            sql = f"SELECT channelid from categories where categoryname=%(categoryname)s;"
            user_data = {
                'categoryname': categoryname,
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


async def dbsetlogchannel(categoryname, value):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"UPDATE categories SET channelid = {value} where categoryname=%(categoryname)s;"
            user_data = {
                'value': value,
                'categoryname': categoryname,
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
