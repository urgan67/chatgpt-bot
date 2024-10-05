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

### Users

# Добавление USER:
async def add_data_user(data):
    connect = None
    try:
        user_id = data.get("user_id")

        if not user_id:
            return False

        keys = ", ".join(data.keys())
        values = list(data.values())

        value = ", ".join([f"${i+1}" for i in range(len(values))])

        execute = f'''
            INSERT INTO users ({keys}) VALUES ({value})
        '''

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
    "user_id": 3,
    "name": "evgen",
    "last_name" : "Urgan"
}

    # Вызов функции для добавления пользователя
# result = asyncio.run(add_data_user(data))
# print("Данные добавлены:", result)



# Чтение USER:
async def get_data_user(data):
    connect = None
    try:
        
        user_id = data.get("user_id")
        if not user_id:
            return "User ID is missing in data"

        connect = await connect_to_db()

        execute = '''
            SELECT * FROM users WHERE user_id = $1;
        '''
        data_user = await connect.fetchrow(execute, user_id)

        if data_user is None:
            return None

        data = dict(data_user)
        return data

    except Exception as e:
        return f"Error getting user data: {e}"

    finally:
        if connect:
            await connect.close()

# result = asyncio.run(get_data_user(data))
# print("Данные пользователя:", result)



# # Обновление данных USERS:
async def update_data_user(data):
    connect = None
    try:
        user_id = data.get("user_id")

        if not user_id:
            return False

        keys, values = [], []

        for key, value in data.items():
            if key != "user_id":
                keys.append(f"{key} = ${len(values) + 1}")
                values.append(value)

        if not keys:
            return False

        key = ", ".join(keys)
        values.append(user_id)

        execute = f'''
            UPDATE users SET {key} WHERE user_id = ${len(values)}
        '''

        connect = await connect_to_db()
        await connect.execute(execute, *values)
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        if connect:
            await connect.close()


# result = asyncio.run(update_data_user(data))
# print("Данные пользователя обновлены:", result)



#### Sessions:

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