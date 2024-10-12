import asyncpg
import asyncio
from keys import user, password, database, host
import logging

async def connect_to_db():
    connect = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        database=database,
    )
    return connect

#### USER TELEGRAM PROPERTY #### 

# Чтение данных USER

async def get_user_by_id(data):
    connect = None
    try:
        user_id = data.get("user_id")
        if not user_id:
            raise ValueError("User ID is missing in data")

        connect = await connect_to_db()

        query = '''
            SELECT * FROM users WHERE user_id = $1;
        '''
        data_user = await connect.fetchrow(query, user_id)

        if data_user is None:
            return None  # Если пользователь не найден, возвращаем None

        # Преобразуем результат в словарь
        user_data = dict(data_user)
        return user_data

    except Exception as e:
        # Здесь можно использовать logging для записи ошибок
        logging.error(f"Error getting user data: {e}")
    finally:
        if connect:
            await connect.close()


# Обновление данных USERS:
async def update_user(data):
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

        query = f'''
            UPDATE users SET {key} WHERE user_id = ${len(values)}
        '''

        connect = await connect_to_db()
        await connect.execute(query, *values)
        return True

    except Exception as e:
        logging.error(f"Failed to update user: {e}")

    finally:
        if connect:
            await connect.close()


# Добавление пользователя в БД
async def adding_user(data):
    connect = None
    try:
        user_id = data.get("user_id")

        if not user_id:
            return False

        keys = ", ".join(data.keys())
        values = list(data.values())

        placeholders = ", ".join([f"${i + 1}" for i in range(len(values))])  # Используем 'placeholders' для ясности

        execute = f'''
            INSERT INTO users ({keys}) VALUES ({placeholders})
        '''

        connect = await connect_to_db()
        await connect.execute(execute, *values)
        logging.info("User added successfully.")
        return True

    except Exception as e:
        logging.error(f"Error adding user: {e}")  # Используем logging вместо print
        return False

    finally:
        if connect:
            await connect.close()  # Закрываем соединение



#### SETTINGS CHATGPT ####

# Read Settings

async def get_settings(id):
    connect = None
    try:
        connect = await connect_to_db()  # Устанавливаем асинхронное соединение с базой данных
        
        query = '''
            SELECT * FROM settings WHERE id = $1;
        '''
        
        # Выполняем запрос и извлекаем результат
        data = await connect.fetchrow(query, id)

        # Если данные найдены, преобразуем их в словарь
        return dict(data) if data else None  # Возвращаем None, если данных нет

    except Exception as e:
        logging.error(f"Ошибка при получении настроек: {e}")
        return None  # Возвращаем None в случае ошибки

    finally:
        if connect:
            await connect.close()  # Закрываем соединение


# Update Settings 

async def update_settings(id, updated_data):
    connect = None
    try:
        # Проверяем, что передан корректный id
        if not id:
            logging.error("ID для обновления настроек не указан.")
            return False

        # Формируем динамический список ключей и значений для обновления
        keys, values = [], []
        for key, value in updated_data.items():
            keys.append(f"{key} = ${len(values) + 1}")  # Формируем параметры запроса $1, $2 и т.д.
            values.append(value)

        # Проверяем, что есть данные для обновления
        if not keys:
            logging.error("Нет данных для обновления.")
            return False

        # Присоединяем условия обновления и добавляем ID в конец списка значений
        set_clause = ", ".join(keys)
        values.append(id)  # Добавляем ID для условия WHERE

        # Создаем SQL-запрос для обновления
        query = f'''
            UPDATE settings SET {set_clause} WHERE id = ${len(values)}
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос
        await connect.execute(query, *values)

        logging.info(f"Настройки с id {id} успешно обновлены.")
        return True  # Возвращаем подтверждение успешного обновления

    except Exception as e:
        logging.error(f"Ошибка при обновлении настроек: {e}")
        return False  # Возвращаем False в случае ошибки

    finally:
        if connect:
            await connect.close()  # Закрываем соединение


# Add to settings User ID

async def add_settings(id):
    connect = None
    try:
        # Проверяем, что передан корректный id
        if not id:
            logging.error("ID для добавления настроек не указан.")
            return False

        # Формируем данные для вставки
        data = {"id": id}

        # Список ключей и значений
        keys = ", ".join(data.keys())  # Например: "id"
        values = list(data.values())   # Список значений для вставки

        # Генерация параметров для запроса ($1, $2 и т.д.)
        value_placeholders = ", ".join([f"${i+1}" for i in range(len(values))])

        # SQL-запрос для вставки данных
        query = f'''
            INSERT INTO settings ({keys}) VALUES ({value_placeholders})
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос
        await connect.execute(query, *values)

        logging.info(f"Настройки для id {id} успешно добавлены.")
        return True  # Возвращаем подтверждение успешного добавления

    except Exception as e:
        logging.error(f"Ошибка при добавлении настроек: {e}")
        return False  # Возвращаем False в случае ошибки

    finally:
        if connect:
            await connect.close()  # Закрываем соединение




####  DISCUSSION ####

# Read Discussion
async def get_discussion(id):
    connect = None
    try:
        # Проверяем, что передан корректный id
        if not id:
            return None

        # SQL-запрос для выборки данных
        query = '''
            SELECT * FROM discussion WHERE id = $1
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос и получаем первую строку данных
        discussion_data = await connect.fetchrow(query, id)

        # Если данные найдены, возвращаем их в виде словаря
        if discussion_data:
            return dict(discussion_data)

        # Если данные не найдены, возвращаем None
        return None

    except Exception as e:
        print(f"Ошибка при получении обсуждения: {e}")
        return None  # Возвращаем None в случае ошибки

    finally:
        if connect:
            await connect.close()  # Закрываем соединение

# Update Discussion 

async def update_discussion(id, updated_data):
    connect = None
    try:
        # Проверяем, что передан корректный id и есть данные для обновления
        if not id or not updated_data:
            return False

        # Формируем части SQL-запроса
        keys, values = [], []
        for key, value in updated_data.items():
            keys.append(f"{key} = ${len(values) + 1}")
            values.append(value)

        # Объединяем части запроса
        set_clause = ", ".join(keys)
        values.append(id)

        # SQL-запрос для обновления данных
        query = f'''
            UPDATE discussion SET {set_clause} WHERE id = ${len(values)}
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос
        await connect.execute(query, *values)

        # Если запрос успешно выполнен, возвращаем True
        return True

    except Exception as e:
        print(f"Ошибка при обновлении обсуждения: {e}")
        return False

    finally:
        if connect:
            await connect.close()  # Закрываем соединение

# Add id to Discussion Table

async def add_discussion(id):
    connect = None
    try:
        # Проверка на наличие id
        if not id:
            return False

        # Данные для вставки
        data = {"id": id}

        # Формирование SQL-запроса
        keys = ", ".join(data.keys())  # Список полей
        values = list(data.values())  # Список значений
        value_placeholders = ", ".join([f"${i+1}" for i in range(len(values))])  # Плейсхолдеры $1, $2 и т.д.

        query = f'''
            INSERT INTO discussion ({keys}) VALUES ({value_placeholders})
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос на добавление данных
        await connect.execute(query, *values)

        # Если запрос успешно выполнен, возвращаем True
        return True

    except Exception as e:
        print(f"Ошибка при добавлении обсуждения: {e}")
        return False

    finally:
        if connect:
            await connect.close()  # Закрываем соединение



#### ECXHANGE ####

# Read exchange

async def get_exchange():
    connect = None
    try:
        # Идентификатор для выборки
        id = 1

        # SQL-запрос для выборки данных
        query = '''
            SELECT * FROM exchange WHERE id = $1
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос и получаем строку данных
        data_exchange = await connect.fetchrow(query, id)

        # Проверяем, если данных нет
        if data_exchange is None:
            return None

        # Преобразуем данные в словарь и возвращаем
        data = dict(data_exchange)
        return data

    except Exception as e:
        print(f"Ошибка при получении данных обмена: {e}")
        return None

    finally:
        if connect:
            await connect.close()  # Закрываем соединение

# Add_exchange

async def add_exchange(data):
    connect = None
    try:
        # Формируем ключи и значения для SQL-запроса
        keys = ", ".join(data.keys())  # Преобразуем ключи словаря в строку через запятую
        values = list(data.values())   # Получаем список значений

        # Формируем строку с плейсхолдерами для значений ($1, $2, ...)
        value_placeholders = ", ".join([f"${i+1}" for i in range(len(values))])

        # SQL-запрос для вставки данных
        query = f'''
            INSERT INTO exchange ({keys}) VALUES ({value_placeholders})
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос
        await connect.execute(query, *values)
        return True

    except Exception as e:
        print(f"Ошибка при добавлении данных в exchange: {e}")
        return False

    finally:
        if connect:
            await connect.close()  # Закрываем соединение

# Update_exchange 

async def update_exchange(id, updated_data):
    connect = None
    try:
        # Проверка наличия данных для обновления
        if not updated_data:
            return False

        # Формируем строки для SQL-запроса
        keys, values = [], []
        for key, value in updated_data.items():
            keys.append(f"{key} = ${len(values) + 1}")
            values.append(value)

        # Соединяем ключи через запятую
        set_clause = ", ".join(keys)
        values.append(id)  # Добавляем id в список значений

        # SQL-запрос для обновления записи
        query = f'''
            UPDATE exchange SET {set_clause} WHERE id = ${len(values)}
        '''
        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос
        await connect.execute(query, *values)
        return True

    except Exception as e:
        print(f"Ошибка при обновлении exchange: {e}")
        return False

    finally:
        if connect:
            await connect.close()  # Закрываем соединение


#### STATISTICS ####
# Add statistics

async def add_statistic(data):
    connect = None
    try:
        # Проверка, что данные для добавления переданы
        if not data:
            return False

        # Формируем строки для вставки
        keys = ", ".join(data.keys())
        values = list(data.values())

        # Формируем строки плейсхолдеров для значений
        placeholders = ", ".join([f"${i+1}" for i in range(len(values))])

        # SQL-запрос для вставки данных в таблицу statistics
        query = f'''
            INSERT INTO statistics ({keys}) VALUES ({placeholders})
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос на добавление данных
        await connect.execute(query, *values)
        return True

    except Exception as e:
        print(f"Ошибка при добавлении статистики: {e}")
        return False

    finally:
        if connect:
            await connect.close()  # Закрываем соединение

# Read Statistics on id all 30 line

async def get_last_30_statistics(user_id):
    connect = None
    try:
        # Проверяем наличие user_id
        if not user_id:
            return None

        # SQL-запрос для получения последних 30 записей статистики для конкретного пользователя
        query = '''
            SELECT * FROM statistics
            WHERE users_telegram_id = $1
            ORDER BY time DESC
            LIMIT 30;
        '''

        # Подключаемся к базе данных
        connect = await connect_to_db()

        # Выполняем запрос с переданным user_id
        rows = await connect.fetch(query, user_id)

        # Преобразуем результат в список словарей
        statistics = [dict(row) for row in rows]
        return statistics

    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")
        return None

    finally:
        if connect:
            await connect.close()  # Закрываем соединение

# ADMIN Read all settings and users an id

async def get_all_stat_admin():
    connect = None
    try:
        # SQL-запрос для получения всех пользователей и их настроек
        query = '''
            SELECT u.user_id, u.username, u.first_name, u.last_name, u.chat_id, 
                   s.temp_chat, s.frequency, s.presence, s.flag_stik, s.all_count, s.all_token, 
                   s.the_gap, s.set_model, s.currency, s.give_me_money, s.money, s.all_in_money
            FROM users u
            JOIN settings s ON u.user_id = s.id;
        '''

        # Подключение к базе данных
        connect = await connect_to_db()

        # Выполняем запрос и получаем все строки
        rows = await connect.fetch(query)

        # Преобразуем строки в список словарей
        data = [dict(row) for row in rows]
        return data

    except Exception as e:
        print(f"Ошибка при получении статистики админа: {e}")
        return None

    finally:
        if connect:
            await connect.close()  # Закрытие соединения

