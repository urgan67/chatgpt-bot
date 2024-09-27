import sqlite3

# Подключение к SQLite базе данных
conn = sqlite3.connect('./db/db.litesql')

try:
    # Создаем объект курсора
    cursor = conn.cursor()

    # Удаляем таблицы (если уже существуют) для избежания конфликтов
    cursor.execute('DROP TABLE IF EXISTS session;')
    cursor.execute('DROP TABLE IF EXISTS users;')

    # Создание таблицы users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50),
        cash REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Создание таблицы session с исправленным синтаксисом
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS session (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tokens REAL,
        price REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    ''')

    # Сохраняем изменения
    conn.commit()

finally:
    # Закрываем соединение
    conn.close()