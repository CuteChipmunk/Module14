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

"""for i in range(10):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?,?,?,?)",
                   (f'new_user{i}', f'{i}x@gmail.com', f'{(i + 1)*10}', f'1000'))"""

for i in range(1, 11, 2):
    cursor.execute("UPDATE Users SET balance = ? WHERE username = ?",(500, f'new_user{i}'))

for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE username = ?",(f'new_user{i}',))

cursor.execute('SELECT * FROM Users WHERE age != 60')
list1 = cursor.fetchall()
for new_user in list1:
    print(f'Имя: {new_user[1]} | Почта: {new_user[2]} | Возраст: {new_user[3]} | Баланс: {new_user[4]}')

connection.commit()
connection.close()

