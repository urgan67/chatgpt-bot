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
# data = {
#     "user_id": 10,
#     "name": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
#     "last_name" : "qqqqqqqq",
#     # "tokens": 100,
#     # "price": 1,
# }

#     # Вызов функции
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

        # Вызов функции
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

        # Вызов функции
# result = asyncio.run(update_data_user(data))
# print("Данные пользователя обновлены:", result)



#### Sessions:

# data_session = {
#     "user_id": 10,
#     "tokens": 10,
#     "price": 1,
#     # "session_id": 1
# }


# Добавление данных в Session:
async def add_data_session(data_session):
    try:

        user_id = data_session.get("user_id")
        if not user_id:
            return False

        # Создаем списки ключей и значений
        keys = ", ".join(data_session.keys())
        values = list(data_session.values())

        # Создаем строку плейсхолдеров вида $1, $2, ..., в зависимости от количества значений
        value = ", ".join([f"${i+1}" for i in range(len(values))])

        # SQL-запрос для вставки данных в таблицу session
        query = f"INSERT INTO session ({keys}) VALUES ({value})"

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос, передавая значения
        await connect.execute(query, *values)

        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        return False

    finally:
        if connect:
            await connect.close()


#     # Вызов функции
# result = asyncio.run(add_data_session(data_session))
# print("Данные для сессии добавлены:", result)


#  Чтение данных Session:

async def get_data_session(user_id):
    connect = None
    try:

        execute = '''
            SELECT * FROM session WHERE user_id = $1;
        '''
        connect = await connect_to_db()
        rows = await connect.fetch(execute, user_id)  # Используем fetch для получения всех строк

        if not rows:
            return f"No session data found for user_id {user_id}"

        data_user = []
        for row in rows:
            data = dict(row)
            data_user.append(data)

        return data_user

    except Exception as e:
        return f"Error getting session data: {e}"

    finally:

        if connect:
            await connect.close()
            


# data_session = {
#     "user_id": 2,
#     "tokens": 10,
#     "price": 1,
#     # "session_id": 1
# }
# tokens = data_session.get('tokens')
# price = data_session.get('price')

result = asyncio.run(get_data_session(10))
print(result)

for dain in result:
    print()
    print(dain.get('tokens'))
    print(dain.get('price'))

