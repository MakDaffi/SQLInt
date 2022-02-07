import pyodbc
from datetime import datetime



connectionString = ("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-PJJGVVN\SQLEXPRESS;"
                      "Database=Dev;"
                      "Trusted_Connection=yes;")

connection = pyodbc.connect(connectionString, autocommit=True)

dbCursor = connection.cursor()

requestString = """SELECT table_name FROM information_schema.tables"""
dbCursor.execute(requestString)
tables = []
for row in dbCursor:
    if row.table_name != 'sysdiagrams':
        tables.append(row.table_name)


