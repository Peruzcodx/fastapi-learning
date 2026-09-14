from database import get_connection

connection = get_connection()

print("database.py connecetd to postgreSQLsuccessfully!")

connection.close()
