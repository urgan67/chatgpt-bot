
# import asyncpg

# async def create_database():
#     # Получаем данные подключения из переменных окружения
#     user = os.getenv('USER_DB')
#     password = os.getenv('PASWOR_DB')
#     # host = os.getenv('DB_HOST', 'localhost')
#     # port = os.getenv('DB_PORT', '5432')

#     try:
#         # Подключаемся к системной базе данных (например, postgres)
#         conn = await asyncpg.connect(
#             user=user,
#             password=password,
#             database='my_database',  # Системная БД для создания новых баз данных
#             # host=host,
#             # port=port
#         )

#         # Проверяем, существует ли уже база данных
#         result = await conn.fetchval(
#             "SELECT 1 FROM pg_database WHERE datname = 'my_database'"
#         )
        
#         if not result:
#             # Создаем базу данных, если она не существует
#             await conn.execute('CREATE DATABASE my_database')
#             print("База данных создана.")
#         else:
#             print("База данных уже существует.")
        
#     except Exception as e:
#         print(f"Ошибка: {e}")
    
#     finally:
#         # Закрываем соединение
#         await conn.close()

    # Создаем новую базу данных
    # await conn.execute('CREATE DATABASE your_database_name')


# Запускаем асинхронную функцию
# asyncio.run(create_database())





# import sqlite3
# conn = sqlite3.connect('./db/db.litesql')

# #### USERS:


# # Получение данных USERS:
# def get_data_user(user_id):
#     try:
#         cursor = conn.cursor()
#         cursor.execute('''
#                 SELECT * FROM users WHERE user_id = ?;
#             ''',
#             (user_id,) 
#         )

#         data_user = cursor.fetchone()

#         data = {}

#         for key, value in zip(cursor.description, data_user):
#             data[key[0]] = value

#         cursor.close()
#         return data
    
#     except Exception as e:
#         return f"Error get data user {e}"


# data = get_data_user(4)
# # print(data)
# # print("user_id:", data.get("user_id"))
# # print("cash:", data.get("cash"))
# # print("name:", data.get("name"))




# # Добавление USERS:
# def add_data_user(data):
#     try:
#         user_id = data.get("user_id")

#         if not user_id:
#             return False

#         keys, values, drop = [], [], []
    
#         for key, value in data.items():
#             keys.append(key)
#             values.append(value)
#             drop.append("?")

#         keys = ", ".join(keys)
#         drop = ", ".join(drop)

#         cursor = conn.cursor()
#         cursor.execute(
#             f'''
#             INSERT INTO users ({keys}) VALUES ({drop}) 
#             ''', 
#             (*values,) 
#         )  # Передаем только values в execute()

#         conn.commit()
#         cursor.close()
#         return True

#     except Exception as e:
#         print(f"Ошибка: {e}")
#         return False 


# # data = {
# #     #"name": 'Anny',
# #     "user_id": 10,
# #     #"cash": 15000,
# # }

# # data = add_data_user(data)
# # print(data)

# # data_2 = get_data_user(10)
# # print(data_2)


# # Обновление данных USERS:
# def update_data_user(data):
#     try:
#         user_id = data.get("user_id")

#         if not user_id:
#             return False

#         key_dict, value_dic = [], []

#         for key, value in data.items():
#             if key != "user_id":
#                 key_dict.append(f"{key} = ?")
#                 value_dic.append(value)

#         if not key_dict:
#             return False

#         key_dict = ", ".join(key_dict)
#         value_dic.append(user_id)

#         cursor = conn.cursor()
#         cursor.execute(
#             f'''
#                 UPDATE users SET {key_dict} WHERE user_id = ?
#             ''',
#                 (*value_dic,)
#         )

#         conn.commit()
#         cursor.close()
#         return True
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return False




# # data = {
# #     #"name": 'Jopa',
# #     "user_id": 8,
# #     #"cash": 3,
# # }

# # data = update_data_user(data)
# # print(data)

# # # data_2 = get_data_user(8)
# # # print(data_2)





# #### Sessions:

# # Добавление Session:
# def add_data_session(data_session):
#     try:
#         user_id = data_session.get("user_id")

#         if not user_id:
#             return False

#         keys, values, drop = [], [], []
    
#         for key, value in data_session.items():
#             keys.append(key)
#             values.append(value)
#             drop.append("?")

#         keys = ", ".join(keys)
#         drop = ", ".join(drop)

#         cursor = conn.cursor()
#         cursor.execute(
#             f'''
#             INSERT INTO session ({keys}) VALUES ({drop}) 
#             ''', 
#             (*values,) 
#         )  # Передаем только values в execute()

#         conn.commit()
#         cursor.close()
#         return True

#     except Exception as e:
#         print(f"Ошибка: {e}")
#         return False 



# # Чтение данных Session:
# def get_data_session(user_id):
#     try:
#         cursor = conn.cursor()
#         cursor.execute('''
#                 SELECT * FROM session WHERE user_id = ?;
#             ''',
#             (user_id,) 
#         )

#         data_user = cursor.fetchall()
#         data_user = []
#         data = {}

#         for key, value in zip(cursor.description, data_user):
#             data[key[0]] = value
#         data_user.append(data)
#         cursor.close()
#         return data
    
#     except Exception as e:
#         return f"Error get data user {e}"
    



# data = get_data_session(4)
# # print("user_id:", data.get("user_id"))
# # print("cash:", data.get("cash"))
# # print("name:", data.get("name"))
# print(data.get('tokens'))
# print(data.get('price'))