import sqlite3

try:
    sqliteConnection = sqlite3.connect('ProjectData.db')
    print("DB Connected")
    cursor = sqliteConnection.cursor()
    cursor.row_factory = sqlite3.Row

    cursor.execute("SELECT * FROM player")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if sqliteConnection:
        sqliteConnection.close()