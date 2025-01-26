import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
    )
    """)

cursor.execute("DELETE FROM Users WHERE id = 6")

cursor.execute("SELECT COUNT(*) FROM Users")
final1 = cursor.fetchone()[0]
print(final1)

cursor.execute("SELECT SUM(balance) FROM Users")
final2 = cursor.fetchone()[0]
print(final2)

cursor.execute("SELECT AVG(balance) FROM Users")
final3 = cursor.fetchone()[0]
print(final3)
#print(final2 / final1)

connection.commit()
connection.close()