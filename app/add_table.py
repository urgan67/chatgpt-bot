import sqlite3

# Подключение к SQLite базе данных
conn = sqlite3.connect('./db/db.litesql')
cursor = conn.cursor()

# Создание таблицы users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50),
    name VARCHAR(50), 
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    cash FLOAT,
    date TIMESTAMP,
    last_active TIMESTAMP
);
''')

# Создание таблицы session
cursor.execute('''
CREATE TABLE IF NOT EXISTS session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
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
# ON DELETE CASCADE?
# Автоматическое удаление зависимых данных: Упрощает удаление данных, связанных с пользователем, без необходимости вручную удалять записи из каждой зависимой таблицы.

# ▎1. Таблица users
# Хранит информацию о пользователях.

# - user_id (Primary Key): Уникальный идентификатор пользователя в Telegram.
# - username: Имя пользователя в Telegram (если доступно).
# - first_name: Имя пользователя.
# - last_name: Фамилия пользователя (если доступно).
# - language_code: Язык пользователя (например, 'en', 'ru').
# - created_at: Дата и время регистрации пользователя.
# - last_active: Дата и время последнего взаимодействия с ботом.


# ▎2. Таблица messages
# Хранит сообщения, отправленные пользователями.

# - message_id (Primary Key): Уникальный идентификатор сообщения.
# - user_id (Foreign Key): Ссылка на пользователя из таблицы users.
# - content: Содержимое сообщения.
# - timestamp: Дата и время отправки сообщения.
# - response_content: Содержимое ответа от бота (если применимо).
# - is_reply: Булевый флаг, указывающий, является ли сообщение ответом на другое сообщение.


# ▎3. Таблица sessions
# Хранит информацию о сессиях пользователей.

# - session_id (Primary Key): Уникальный идентификатор сессии.
# - user_id (Foreign Key): Ссылка на пользователя из таблицы users.
# - start_time: Дата и время начала сессии.
# - end_time: Дата и время окончания сессии.
# - context: Хранит контекст или состояние сессии (например, в формате JSON).

# 4. Таблица preferences
# Хранит настройки и предпочтения пользователей.

# - preference_id (Primary Key): Уникальный идентификатор предпочтения.
# - user_id (Foreign Key): Ссылка на пользователя из таблицы users.
# - key: Ключ настройки (например, 'notifications_enabled').
# - value: Значение настройки (например, 'true' или 'false').


# 5. Таблица errors
# Хранит информацию об ошибках, возникших при взаимодействии с ботом.

# - error_id (Primary Key): Уникальный идентификатор ошибки.
# - user_id (Foreign Key): Ссылка на пользователя из таблицы users.
# - error_message: Описание ошибки.
# - timestamp: Дата и время возникновения ошибки.

#  Таблица user_roles
#    - role_id (Primary Key): Уникальный идентификатор роли.
#    - user_id (Foreign Key): Ссылка на пользователя из таблицы users.
#    - role_name: Название роли (например, "администратор", "модератор").
#    - assigned_at: Дата и время назначения роли.

# Таблица statistics
#    - stat_id (Primary Key): Уникальный идентификатор статистики.
#    - user_id (Foreign Key): Ссылка на пользователя из таблицы users.
#    - interaction_count: Количество взаимодействий с ботом.
#    - last_interaction_date: Дата последнего взаимодействия.