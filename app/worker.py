
import sqlite3
conn = sqlite3.connect('./db/db.litesql')

#### USERS:

# Чтение USERS:
def get_data_user(data):

    try:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT * FROM users WHERE user_id = ?;
            ''',
            (data['user_id'],) 
        )
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as e:
        return f"Error get data user {e}"

# Добавление в USERS:
def add_data_user(data):

    try:
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO users (user_id, name, cash)
                VALUES (?, ?, ?)
            ''',
            (data.get('user_id'), data.get('name'), data.get('cash'))
        )
        conn.commit()
        cursor.close()
        return True
    except:
        return False

# Update Users:
def update_data_user(data):

    try:
        cursor = conn.cursor()
        cursor.execute('''
                UPDATE user SET user_id = ?;
            ''',
            (data.get('user_id'), data.get('name'), data.get('cash'))
        )
        conn.commit()
        cursor.close()
        return f"{cursor.rowcount} record(s) updated."
    except Exception as e:
        return f"Error updating user data: {e}"



#### SESSIONS:

# Add session:

def add_session(conn, data, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE user_id = ?;', (user_id,))
        user = cursor.fetchone()
        if user is None:
            print(f"Пользователь с user_id {data} не найден.")
            return False

        cursor.execute('''
            INSERT INTO session (user_id, model, tokens, price)
            VALUES (?, ?, ?, ?);
        ''', (data.get('user_id'))
        )
        conn.commit()
        print(f"Сессия для пользователя с user_id {data} успешно добавлена.")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении сессии для пользователя с user_id {data}: {e}")
        return False
    
# Read sessions:

# def get_sessions(conn, user_id):
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM session WHERE user_id = ?;', (user_id,))
#     sessions = cursor.fetchall()
#     cursor.close()



# # Функция для добавления сессии
# def add_session(conn, user_id, model, tokens=0, price=0.0):
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM users WHERE id = ?;', (user_id,))
    
#     if cursor.fetchone() is None:
#         print(f"Пользователь с user_id {user_id} не найден.")
#         cursor.close()
#         return False

#     cursor.execute('''
#         INSERT INTO session (user_id, model, tokens, price)
#         VALUES (?, ?, ?, ?);
#     ''', (user_id, model, tokens, price))
#     conn.commit()
#     cursor.close()
    
#     print(f"Сессия для пользователя с user_id {user_id} успешно добавлена.")
#     return True
# #             ### Функция для добавления сессии ###
# # def add_session(conn, user_id, model, tokens=0, price=0.0):
# #     cursor = conn.cursor()
# #     try:
# #         cursor.execute('SELECT * FROM users WHERE user_id = ?;', (user_id,))
# #         user = cursor.fetchone()
# #         if user is None:
# #             print(f"Пользователь с user_id {user_id} не найден.")
# #             return False

# #         cursor.execute('''
# #             INSERT INTO session (user_id, model, tokens, price)
# #             VALUES (?, ?, ?, ?);
# #         ''', (user_id, model, tokens, price))
# #         conn.commit()
# #         print(f"Сессия для пользователя с user_id {user_id} успешно добавлена.")
# #         return True
# #     except sqlite3.Error as e:
# #         print(f"Ошибка при добавлении сессии для пользователя с user_id {user_id}: {e}")
# #         return False

# # Функция для получения всех сессий пользователя
# def get_sessions(conn, user_id):
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM session WHERE user_id = ?;', (user_id,))
#     sessions = cursor.fetchall()
#     cursor.close()

#     if sessions:
#         print(f"Найдено {len(sessions)} сессий для пользователя с user_id {user_id}.")
#     else:
#         print(f"Для пользователя с user_id {user_id} сессий не найдено.")
    
#     return sessions
# #                 ### Функция для получения всех сессий пользователя ###
# # def get_sessions(conn, user_id):
# #     cursor = conn.cursor()
# #     try:
# #         cursor.execute('SELECT * FROM session WHERE user_id = ?;', (user_id,))
# #         sessions = cursor.fetchall()
# #         if sessions:
# #             print(f"Найдено {len(sessions)} сессий для пользователя с user_id {user_id}.")
# #         else:
# #             print(f"Для пользователя с user_id {user_id} сессий не найдено.")
# #         return sessions
# #     except sqlite3.Error as e:
# #         print(f"Ошибка при получении сессий для пользователя с user_id {user_id}: {e}")
# #         return []
