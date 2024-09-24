import sqlite3

# Подключение к SQLite базе данных
conn = sqlite3.connect('./db/db.litesql')
cursor = conn.cursor()

# Создание таблицы users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50), 
    cash FLOAT,
    date TIMESTAMP
);
''')

# Создание таблицы session
cursor.execute('''
CREATE TABLE IF NOT EXISTS session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    model VARCHAR(50),
    tokens INTEGER,
    price FLOAT,
    date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
''')

# Зафиксировать изменения и закрыть соединение
conn.commit()
conn.close()





# # name - unique 
# # Тип REAL используется, чтобы поддерживать не только целые числа, но и дробные значения (например, 150.50).
# # TIMESTAMP: хранит дату и время с автоматическим учетом часового пояса и возможности отслеживания изменений в записи.
# # CURRENT_TIMESTAMPЧтобы автоматически устанавливать текущую дату при добавлении записи, можно использовать функцию CURRENT_DATE (для даты) или CURRENT_TIMESTAMP (для даты и времени):

# # foreign key                                   -- Внешний ключ связывает с таблицей users
# # user_id INTEGER,                              -- Внешний ключ, ссылающийся на пользователя
# # session_id INTEGER PRIMARY KEY AUTOINCREMENT  -- Добавляем идентификатор для каждой сессии

