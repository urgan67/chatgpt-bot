
import sqlite3
conn = sqlite3.connect('./db/db.litesql')

# data = {
#     "user_id": 21258098,
#     "name": 'Ann',
#     "cash": 10,
# }
# user_id = data.get('user_id')
# name = data.get('name')
# cash = data.get('cash')

#### USERS: ####

# Чтение USERS:
def get_data_user(user_id):

    try:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT * FROM users WHERE user_id = ?;
            ''',
            (user_id,)
        )
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as e:
        return f"Error get data user {e}"

# Добавление в USERS:
def add_data_user(user_id, name, cash):

    try:
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO users (user_id, name, cash)
                VALUES (?, ?, ?)
            ''',
            (user_id = data.get('user_id'), name = data.get('name'), cash = data.get('cash'))
        )
        conn.commit()
        cursor.close()
        return True
    except:
        return False

# Update Users:




#### SESIONS: ####

# Read sesion:




    # if user:
    #     print(f"Пользователь с user_id {user_id} найден: {user}")
    # else:
    #     print(f"Пользователь с user_id {user_id} не найден.")
# #                     ### Функция для получения пользователя по user_id ###
# # def get_user(conn, user_id):
# #     cursor = conn.cursor()
# #     try:
# #         cursor.execute('SELECT * FROM users WHERE user_id = ?;', (user_id,))
# #         user = cursor.fetchone()
# #         if user:
# #             print(f"Пользователь с user_id {user_id} найден: {user}")
# #         else:
# #             print(f"Пользователь с user_id {user_id} не найден.")
# #         return user
# #     except sqlite3.Error as e:
# #         print(f"Ошибка при получении пользователя с user_id {user_id}: {e}")
# #         return None
# # cursor.close()


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
# def base():
#     mock_conn = MagicMock()

#     # Добавление пользователей
#     add_user(mock_conn, 'Nick', 50.0)
#     # add_user(mock_conn, 'Alice', 100.0)

#     # Получение и работа с пользователями
#     get_user(mock_conn, 1)
#     # add_session(mock_conn, 1, 'model1')
#     # get_sessions(mock_conn, 1)

#     # get_user(mock_conn, 2)
#     add_session(mock_conn, 2, 'model2')
#     get_sessions(mock_conn, 2)

# if __name__ == '__main__':
#     base()
# # Закрываем соединение с базой данных
# conn.close()
