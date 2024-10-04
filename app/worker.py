import asyncpg
import asyncio
from keys import user, password, database, host

async def connect_to_db():
    connect = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        database=database,
    )
    return connect


# Добавление USERS:

async def add_data_user(data):
    connect = None
    try:
        user_id = data.get("user_id")

        if not user_id:
            return False

        keys, values, value = [], [], []





        keys = ", ".join(data.keys())
        # value = ", ".join(["?"] * len(data)) 
        values = tuple(data.values())

        execute = f'''
            INSERT INTO users ({keys}) VALUES ($1, $2, $3)
        '''
        
        print(f"SQL запрос: {execute}") 
        print(f"Значения: {values}")  

        # Выполнение запроса
        connect = await connect_to_db()
        await connect.execute(execute, *values)
        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    finally:
        if connect:
            await connect.close()

# Данные для добавления
data = {
    "user_id": 2,
    "name": "Anton",
    "last_name" : "ivanov"
}

    # Вызов функции для добавления пользователя
result = asyncio.run(add_data_user(data))
print("Данные добавлены:", result)

# def add_data_user(data):
#     try:
#         user_id = data.get("user_id")

#         if not user_id:
#             return False

#         keys = ", ".join(data.keys())
#         value = ", ".join(["?"] * len(data))
#         values = tuple(data.values())

#         execute = f'''
#             INSERT INTO users ({keys}) 
#             VALUES ({value}) 
#         '''

#         # Выполнение запроса
#         connect = await connect_to_db()
#         await connect.execute(execute, *values) 
#         return True

#     except Exception as e:
#         print(f"Ошибка: {e}")
#         return False
#     finally:
#         if connect:
#             await connect.close() 


     







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



# # #### USERS:


# # Получение данных USERS:

# async def get_data_user(user_id):
#     try:
#         # Устанавливаем подключение к базе данных (conn должно быть асинхронным)
#         conn = await asyncpg.connect(
#         user=user,
#         password=password,
#         host=host,
#         port=port,
#         database=database
#         )

#         # Выполняем асинхронный запрос к базе данных
#         query = '''
#             SELECT * FROM users WHERE user_id = $1;
#         '''
#         data_user = await conn.fetchrow(query, user_id)

#         # Если данные пользователя не найдены, возвращаем None
#         if data_user is None:
#             return None

#         # Преобразуем результат запроса в словарь
#         data = dict(data_user)

#         # Закрываем подключение
#         await conn.close()

#         return data

#     except Exception as e:
#         return f"Error get data user: {e}"



# # data = get_data_user(4)
# # print(data)
# # print("user_id:", data.get("user_id"))
# # print("cash:", data.get("cash"))
# # print("name:", data.get("name"))


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