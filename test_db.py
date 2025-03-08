import MySQLdb

try:
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        password='root',
        db='lab_db'
    )
    print("Successfully connected to MySQL!")
    connection.close()
except Exception as e:
    print(f"Error connecting to MySQL: {e}") 