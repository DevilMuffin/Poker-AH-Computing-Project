import sqlite3

try:
    sqliteConnection = sqlite3.connect('ProjectData.db')
    cursor = sqliteConnection.cursor()

    cursor.execute("""INSERT INTO player VALUES ('Player', 200, 3, 5, 6)""")
    cursor.execute("""INSERT INTO player VALUES ('Bob', 123, 7, 8, 9)""")
    cursor.execute("""INSERT INTO player VALUES ('Alice', 5423, 6, 7, 3)""")
    cursor.execute("""INSERT INTO player VALUES ('James', 12314, 23, 65, 25)""")
    cursor.execute("""INSERT INTO player VALUES ('Jacob', 231, 321, 123, 1234)""")
    cursor.execute("""INSERT INTO player VALUES ('Scott', 54, 4, 23, 32)""")

    sqliteConnection.commit()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
