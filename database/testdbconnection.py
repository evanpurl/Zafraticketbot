from mysql.connector import Error, MySQLConnection
from database.python_mysql_dbconfig import read_db_config


async def connect():  # Initial DB connection test
    """ Connect to MySQL database """

    db_config = read_db_config()
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except Error as error:
        print("error")
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')