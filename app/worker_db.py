import asyncpg
import asyncio
from aiogram.types import Message
from keys import user_db, paswor_db, database, host
import logging
import openai
from gtts import gTTS

async def connect_to_db():
    connect = await asyncpg.connect(
        user=user_db,
        password=paswor_db,
        host=host,
        database=database,
    )
    return connect


#### USER TELEGRAM PROPERTY #### 

# Read User Telegram Data
async def get_user_by_id(id):
    # Создаем подключение к базе данных
    conn = await connect_to_db()
    
    try:
        # Выполняем запрос на выборку данных пользователя по переданному id
        query = "SELECT * FROM users_telegram WHERE id = $1"
        data = await conn.fetchrow(query, id)
        
        # Возвращаем результат или None, если пользователь не найден
        return data or None
    finally:
        # Закрываем подключение
        await conn.close()



# Update User Telegram
async def update_user(id, updated_data):
    # Создаем подключение к базе данных
    conn = await connect_to_db()
    
    confirmation = False
    try:
        # Строим динамический запрос для обновления данных
        set_clause = ", ".join([f"{key} = ${index+1}" for index, key in enumerate(updated_data.keys())])
        values = list(updated_data.values())
        
        # Выполняем запрос на обновление данных
        query = f"UPDATE users_telegram SET {set_clause} WHERE id = ${len(values) + 1}"
        await conn.execute(query, *values, id)
        
        confirmation = True
        logging.info(f"update_user {id}")
    except Exception as e:
        logging.error(f"Failed to update user: {e}")
    finally:
        # Закрываем подключение
        await conn.close()

    return confirmation



# Add User Telegram to DB
async def adding_user(user_data):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Строим запрос для добавления нового пользователя
        columns = ", ".join(user_data.keys())
        values_placeholder = ", ".join([f"${i+1}" for i in range(len(user_data))])
        query = f"INSERT INTO users_telegram ({columns}) VALUES ({values_placeholder})"
        
        # Выполняем запрос на добавление пользователя
        await conn.execute(query, *user_data.values())
        
        confirmation = True
        logging.info("User added successfully")
    except Exception as e:
        logging.error(f"Failed to add user: {e}")
    finally:
        await conn.close()

    return confirmation




#### SETTINGS CHATGPT ####

# Read Settings
async def get_settings(id):
    conn = await connect_to_db()
    try:
        # Выполняем запрос на выборку настроек по переданному id
        query = "SELECT * FROM settings WHERE id = $1"
        data = await conn.fetchrow(query, id)
        
        # Возвращаем данные или None, если запись не найдена
        return data or None
    except Exception as e:
        logging.error(f"Failed to get settings for id {id}: {e}")
        return None
    finally:
        await conn.close()


# Update Settings 
async def update_settings(id, updated_data):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Строим динамический запрос для обновления данных
        set_clause = ", ".join([f"{key} = ${index+1}" for index, key in enumerate(updated_data.keys())])
        values = list(updated_data.values())
        
        # Добавляем id в конец значений
        query = f"UPDATE settings SET {set_clause} WHERE id = ${len(values) + 1}"
        await conn.execute(query, *values, id)
        
        confirmation = True
        logging.info(f"Update Settings for id {id}")
    except Exception as e:
        logging.error(f"Failed to update settings for id {id}: {e}")
    finally:
        await conn.close()

    return confirmation


# Add to settings User ID
async def add_settings(id):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Строим запрос для добавления настроек с переданным id
        query = "INSERT INTO settings (id) VALUES ($1)"
        
        # Выполняем запрос
        await conn.execute(query, id)
        
        confirmation = True
        logging.info(f"Settings added for user with id {id}")
    except Exception as e:
        logging.error(f"Failed to add settings for id {id}: {e}")
    finally:
        await conn.close()

    return confirmation


####  DISCUSSION ####

# Get Discussion by ID
async def get_discussion(id):
    conn = await connect_to_db()
    try:
        # Выполняем запрос на выборку обсуждения по переданному id
        query = "SELECT * FROM discussion WHERE id = $1"
        data = await conn.fetchrow(query, id)
        
        # Возвращаем данные или None, если запись не найдена
        return data or None
    except Exception as e:
        logging.error(f"Failed to get discussion for id {id}: {e}")
        return None
    finally:
        await conn.close()



# Update Discussion 
async def update_discussion(id, updated_data):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Строим динамический запрос для обновления данных
        set_clause = ", ".join([f"{key} = ${index+1}" for index, key in enumerate(updated_data.keys())])
        values = list(updated_data.values())
        
        # Выполняем запрос на обновление данных
        query = f"UPDATE discussion SET {set_clause} WHERE id = ${len(values) + 1}"
        await conn.execute(query, *values, id)
        
        confirmation = True
        logging.info(f"Update Discussion for id {id}")
    except Exception as e:
        logging.error(f"Failed to update discussion for id {id}: {e}")
    finally:
        await conn.close()

    return confirmation



# Add id to Discussion Table
async def add_discussion(id):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Строим запрос для добавления id в таблицу discussion
        query = "INSERT INTO discussion (id) VALUES ($1)"
        
        # Выполняем запрос на добавление данных
        await conn.execute(query, id)
        
        confirmation = True
        logging.info(f"add_discussion {id}")
    except Exception as e:
        logging.error(f"Failed to add id Discussion: {e}")
    finally:
        await conn.close()

    return confirmation


#### ECXHANGE ####

# Get Exchange rate by ID
async def get_exchange():
    conn = await connect_to_db()
    id = 1
    try:
        # Выполняем запрос на выборку данных из таблицы exchange по id
        query = "SELECT * FROM exchange WHERE id = $1"
        data = await conn.fetchrow(query, id)
        
        # Возвращаем результат или None, если данные не найдены
        return data or None
    except Exception as e:
        logging.error(f"Failed to get exchange data for id {id}: {e}")
        return None
    finally:
        await conn.close()



# Add exchange rate
async def add_exchange(data):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Формируем запрос для добавления данных
        query = """
        INSERT INTO exchange (timestamp, rate) 
        VALUES ($1, $2)
        """
        
        # Выполняем запрос на добавление данных в таблицу exchange
        await conn.execute(query, data['timestamp'], data['rate'])
        
        confirmation = True
        logging.info("Add_exchange")
    except Exception as e:
        logging.error(f"Failed to add Exchange rate: {e}")
    finally:
        # Закрываем соединение
        await conn.close()

    return confirmation



# Update exchange rate by ID
async def update_exchange(id, updated_data):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Формируем динамический запрос для обновления данных
        set_clause = ", ".join([f"{key} = ${index+1}" for index, key in enumerate(updated_data.keys())])
        values = list(updated_data.values())
        
        # Строим запрос на обновление
        query = f"UPDATE exchange SET {set_clause} WHERE id = ${{len(values) + 1}}"
        
        # Выполняем запрос на обновление данных
        await conn.execute(query, *values, id)
        
        confirmation = True
        logging.info(f"Update_exchange {id}")
    except Exception as e:
        logging.error(f"Failed to update Exchange rate: {e}")
    finally:
        # Закрываем соединение
        await conn.close()

    return confirmation



#### STATISTICS ####

# Add a new statistic record dynamically
async def add_statistic(data):
    conn = await connect_to_db()
    confirmation = False
    try:
        # Извлекаем ключи и значения из словаря
        keys = data.keys()
        values = data.values()
        
        # Динамически создаем часть запроса для полей (ключей) и их значений (плейсхолдеров $1, $2, ...)
        columns = ", ".join(keys)
        placeholders = ", ".join([f"${i+1}" for i in range(len(keys))])

        # Формируем запрос на добавление данных
        query = f"INSERT INTO statistics ({columns}) VALUES ({placeholders})"
        
        # Выполняем запрос с динамически созданными плейсхолдерами и значениями
        await conn.execute(query, *values)
        
        confirmation = True
        logging.info("Successfully added a new statistics record.")
    except Exception as e:
        logging.error(f"Failed to add statistics: {e}")
    finally:
        # Закрываем соединение
        await conn.close()

    return confirmation



# Read last 30 lines of statistics for a user
async def get_last_30_statistics(id):
    conn = await connect_to_db()
    try:
        # Формируем запрос для выборки последних 30 строк статистики пользователя с сортировкой по дате
        query = """
            SELECT * 
            FROM statistics
            WHERE users_telegram_id = $1
            ORDER BY time DESC
            LIMIT 30
        """
        
        # Выполняем запрос и получаем результат
        data = await conn.fetch(query, id)
        
        # Возвращаем все строки данных
        return data
    except Exception as e:
        logging.error(f"Failed to fetch last 30 statistics for user {id}: {e}")
        return None
    finally:
        # Закрываем соединение с базой данных
        await conn.close()



# ADMIN Read all settings and users using dictionary
async def get_all_stat_admin():
    conn = await connect_to_db()
    try:
        # SQL-запрос для получения данных из users_telegram и связанных настроек из таблицы settings
        query = """
            SELECT u.*, s.*
            FROM users_telegram u
            JOIN settings s ON u.id = s.id
        """
        
        # Выполнение запроса и получение всех строк
        data = await conn.fetch(query)

        # Преобразуем результат в список словарей
        results = []
        for row in data:
            row_dict = dict(row)  # Преобразуем объект строки в словарь
            results.append(row_dict)
        
        # Логирование для проверки
        for result in results:
            logging.info(f"User and Settings Data: {result}")
        
        return results
    except Exception as e:
        logging.error(f"Failed to fetch all user stats for admin: {e}")
        return None
    finally:
        # Закрываем соединение с базой данных
        await conn.close()


####VOICE####

# Функция для работы с базой данных (сохранение голосового сообщения)
async def save_voice_message_to_db(message: Message, transcript, gpt_response):
    # Подключаемся к базе данных
    conn = await connect_to_db()

    # Извлекаем необходимые данные автоматически из объекта message
    chat_id = message.chat.id
    file_id = message.voice.file_id

    try:
        # Вставляем данные в таблицу voice_messages
        await conn.execute('''
            INSERT INTO voice_messages (chat_id, file_id, transcript, gpt_response)
            VALUES ($1, $2, $3, $4)
        ''', chat_id, file_id, transcript, gpt_response)
        logging.info(f"Запись о голосовом сообщении добавлена в базу данных для чата {chat_id}")
    
    except Exception as e:
        logging.error(f"Ошибка при сохранении голосового сообщения в базе данных: {e}")
    
    finally:
        await conn.close()


# ###voice###
# # Функция для преобразования речи в текст (STT)
# async def stt(file_path: str):
#     try:
#         # Использование актуального интерфейса OpenAI для транскрипции
#         with open(file_path, "rb") as audio_file:
#             transcription = openai.Audio.transcribe(
#                 model="whisper-1",  # Использование модели Whisper для транскрипции
#                 file=audio_file,
#                 language="ru",  # Язык, на котором записано сообщение
#             )
#         return transcription.get('text', '')  # Возвращаем текст из транскрипции
#     except openai.OpenAIError as e:
#         print(f"Error during transcription: {e}")
#         return ''
            

# # Функция для конвертации текста в речь
# async def tts(text: str, save_path: str):
#     try:
#         # Преобразуем текст в речь (пример с использованием gTTS или pyttsx3)
#         from gtts import gTTS
#         tts = gTTS(text=text, lang='ru')
#         tts.save(save_path)
#         print(f"Speech saved to {save_path}")
#     except Exception as e:
#         print(f"Error during text-to-speech conversion: {e}")


# # Функция для запроса GPT на основе текста
# async def ask_gpt(text: str):
#     """ Функция для отправки текста в GPT и получения ответа """
#     try:
#         response = openai.Completion.create(
#             model="gpt-4",  # Выберите подходящую модель GPT
#             prompt=text,
#             max_tokens=150
#         )
#         return response.choices[0].text.strip() if response.choices else None
#     except openai.error.OpenAIError as e:
#         print(f"OpenAI error while asking GPT: {e}")
#         return None