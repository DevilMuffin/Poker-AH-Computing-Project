import sqlite3

try:
    sqliteConnection = sqlite3.connect('PokerData.db')
    print("DB Connected")
    cursor = sqliteConnection.cursor()


    insertQuery = '''UPDATE player SET chipValue= ?,wins = ?,losses = ?,betsPlaced = ? WHERE name = ?'''

    cursor.execute(insertQuery, (125, 3, 2, 10, "Alasdair"))
    cursor.execute(insertQuery, (250, 5, 3, 14, "Bob"))
    cursor.execute(insertQuery, (135, 2, 5, 20, "Alice"))
    
    sqliteConnection.commit()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("DB Closed")