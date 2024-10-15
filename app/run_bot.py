import logging

from keys import (
    token, api_key, white_list, admin_user_ids,
    block,#, receiver_yoomoney, token_yoomoney, wallet_pay_token
                   )
from about_bot import about_text
from terms_of_use import terms
import time
import sys
import re
import os
import asyncio
from pathlib import Path
from openai import AsyncOpenAI, RateLimitError, OpenAIError
from aiogram import Bot, Dispatcher, types, F, Router
# from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, FSInputFile, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, Voice)


from aiogram.enums import ParseMode, ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment

import aiofiles
import openai
import csv
import datetime
from io import StringIO, BytesIO
from get_time import get_time
from calculation import calculation
from backupdb import backup_db
from restore_db import restore_db
from add_money import add_money_by_card, add_money_wallet_pay, add_money_cripto

from worker_db import (
    adding_user, get_user_by_id, update_user, add_settings, add_discussion, update_settings,
    get_settings, get_discussion, update_discussion, get_exchange, update_exchange, get_last_30_statistics,
    get_all_stat_admin, save_voice_message_to_db#, stt, tts, ask_gpt
)
from keyboards import (
    main_menu, sub_setings, sub_balance, back_to_main, back_to_setings,\
    sub_setings_model, sub_setings_time, sub_setings_creativ, sub_setings_repet, sub_setings_repet_all,\
    sub_add_money, admin_menu, confirm_summ
)


client = AsyncOpenAI(api_key=api_key)
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls
router = Router()
openai.api_key = api_key
# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing - для обращения к OpenAI другая функция которая запускается вместе с...
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')
    # await asyncio.sleep(5)


# PUSH /START
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    # Меню
    bot_commands = [
        BotCommand(command="/menu", description="Главное меню | Main Menu"),
        # BotCommand(command="/sub_dialog", description="Сброс диалога | Resetting the dialog"),
        # BotCommand(command="/model", description="Выбрать модель GPT | Choose a GPT model"),
    ]
    await bot.set_my_commands(bot_commands)


    # name = user.name  Shliamb

    ###### Get All data user on telegram ######
    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    is_admin = False
    is_block = False
    is_good = 3
    admin_id = admin_user_ids[1:-1]
    ###### Get All data user on telegram ######

    logging.info(f"User {id} press /start")

    # Checking and added the parameters
    if str(id) in admin_user_ids:
        is_admin = True
        logging.info(f"The user id:{id} is assigned as an admin.")

    # Preparing data for the user
    user_data = {"id": id, "name": name, "full_name": full_name, "first_name":first_name,\
                    "last_name": last_name, "chat_id": chat_id, "is_admin": is_admin,\
                    "is_block":is_block, "is_good": is_good}
    
    # If user id has in a Base - update data, else - create user to Base
    is_on_user = await get_user_by_id(id)
    if is_on_user is not None:
        await update_user(id, user_data)
    else:
        await adding_user(user_data)
        await add_settings(id)
        await add_discussion(id)
    
    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "bro"))

    # Checking and added the parameters in Settings to white list users And gives them money
    if str(id) in white_list:
        money = 1000 # Yep!
        updated_data = {"money": money}
        confirmation = await update_settings(id, updated_data) # Gives money
        if confirmation is True: # Подтверждение из worcker_db
            logging.info(f"1000 RUB added, he id is:{id}.")
        else:
            logging.error(f"A 1000 RUB has not added, he id is:{id}.")

    await message.answer(f"Привет {about}! Я *ChatGPT*. Мне можно сразу задать вопрос или настроить - /setup. Там же можно выбрать последнюю модель ChatGPT.\nHello {about}! I am *ChatGPT*. You can ask me a question right away or set up - /setup. You can also select the latest ChatGPT model there.")


    #### WORK MENU ADMIN ####
# Admin statistic menu /admin
@dp.message(Command("admin"))
async def admin(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)
    user = await get_user_by_id(id)
    if user:
        is_admin = user['is_admin']
    if  is_admin is True:
        await admin_menu(bot, message)
    else:
        logging.info(f"User id:{id} tried to log into the admin panel.")




# Admin submenu stat
@dp.callback_query(lambda c: c.data == 'admin_stat')
async def process_sub_admin_stat(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id  # Получаем user_id из callback_query
    chat_id = callback_query.message.chat.id
    
    # Получаем все статистики для админа
    data = await get_all_stat_admin()

    all_static = []
    number = 0
    all_static.append(["№", "Имя", "id", "Полное имя", "Первое имя", "Второе имя", "Админ",\
                        "Заблок", "Колл. вопросов", "Исп. токенов за все время", "Модель по умолч.",\
                              "Дата запроса на пополнение","Сумма запроса","Валюта запроса", "Баланс", "Внесенно денег за все время", "Статистика ниже ответа",\
                                  "Время по умолчанию"])  # First a names row
    
    for row in data:
        # Извлекаем данные из словаря
        user_id = row['id']  # id из users_telegram
        name = row['name']  # Имя из users_telegram
        full_name = row['full_name']  # Полное имя из users_telegram
        first_name = row['first_name']  # Первое имя из users_telegram
        last_name = row['last_name']  # Второе имя из users_telegram
        is_admin = row['is_admin']  # Админ из users_telegram
        is_block = row['is_block']  # Заблокирован ли из users_telegram
        is_good = row['is_good']  # Статус из users_telegram
        
        # Извлекаем данные из настроек (settings)
        all_count = row['all_count']  # Количество вопросов из settings
        all_token = row['all_token']  # Токены из settings
        the_gap = row['the_gap']  # Промежуток времени из settings
        set_model = row['set_model']  # Модель по умолчанию из settings
        time_money = row['time_money']  # Время денег из settings
        give_me_money = row['give_me_money']  # Запрос на деньги из settings
        currency = row['currency']  # Валюта из settings
        money = round(row['money'], 2)  # Баланс из settings
        all_in_money = round(row['all_in_money'], 2)  # Все деньги из settings
        flag_stik = row['flag_stik']  # Статус из settings

        # Добавляем данные в список
        number += 1
        all_static.append([number, name, user_id, full_name, first_name, last_name, is_admin, is_block, all_count,
                            all_token, set_model, time_money, give_me_money, currency, money, all_in_money, flag_stik, the_gap])

    # Создание csv файла
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()

    # Отправка csv файла
    file_name = f"Admin-{datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=chat_id, document=buffered_input_file)
        await bot.answer_callback_query(callback_query.id)
    except Exception as e:
        print(f"Error sending document: {e}")

# # Back to main
# @dp.callback_query(lambda c: c.data == 'back_to_main')
# async def process_back_to_main(callback_query: types.CallbackQuery):
#     await back_to_main(bot, callback_query)
#     await bot.answer_callback_query(callback_query.id)

# Close menu
@dp.callback_query(lambda c: c.data == 'close_admin')
async def close_admin_menu(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=chat_id, message_id=message_id) # Удалить и меню и сообщение
    await bot.answer_callback_query(callback_query.id)


# Admin submenu download log
@dp.callback_query(lambda c: c.data == 'admin_get_log')
async def process_sub_admin_stat(callback_query: types.CallbackQuery):

    if os.path.exists("./log/app.log") and os.path.getsize("./log/app.log") > 0:
        await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile("./log/app.log"))
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.send_message(callback_query.from_user.id, "Файл app.log пустой или отсуствует.")
        await bot.answer_callback_query(callback_query.id)


# Admin clear log /clearlog
@dp.callback_query(lambda c: c.data == 'admin_clear_log')
async def process_sub_admin_stat(callback_query: types.CallbackQuery):

    if os.path.exists("./log/app.log") and os.path.getsize("./log/app.log") > 0:

        with open("./log/app.log", 'w'):
            pass
        await bot.send_message(callback_query.from_user.id, "Файл app.log очищен успешно.")
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.send_message(callback_query.from_user.id, "Файл app.log пустой или отсуствует.")
        await bot.answer_callback_query(callback_query.id)


# Admin BackupDB
@dp.callback_query(lambda c: c.data == 'backup')
async def process_sub_admin_stat(callback_query: types.CallbackQuery):
    # Создаем резервную копию базы данных
    confirmation = backup_db()  # - резервная копия
    if confirmation:
        await bot.send_message(callback_query.from_user.id, "Резервная копия базы данных создана успешно и представленна ниже. Сохранены 3 последние версии в рабочей папке, остальные удалены.")
    else:
        await bot.send_message(callback_query.from_user.id, "Ошибка создания резервной копии базы данных.")

    # Делаем небольшую задержку перед отправкой файла
    await asyncio.sleep(0.5)

    # Папка с резервными копиями
    data_folder = Path("./backup_db/")

    # Получаем список всех файлов в директории
    files = [entry for entry in data_folder.iterdir() if entry.is_file()]

    # Сортируем список файлов по дате изменения (от новых к старым)
    sorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)

    # Удаляем все старые файлы, оставляем последние 3
    for file_to_delete in sorted_files[3:]:
        os.remove(file_to_delete)
    logging.info("Удалены старые файлы, оставлены 3 последних.")

    # Получаем последний файл (самый новый)
    last_downloaded_file = sorted_files[0] if sorted_files else None

    if last_downloaded_file and last_downloaded_file.stat().st_size > 0:  # Проверяем, что файл существует и не пуст
        try:
            logging.info(f"Отправка последнего файла базы данных: {last_downloaded_file}")
            await bot.send_document(chat_id=callback_query.from_user.id, document=InputFile(last_downloaded_file))
        except Exception as e:
            logging.error(f"Ошибка при отправке файла: {e}")
            await bot.send_message(callback_query.from_user.id, "Ошибка при отправке резервной копии.")
    else:
        logging.error("Файл пустой или не существует.")
        await bot.send_message(callback_query.from_user.id, "Резервная копия базы данных не найдена или пустая.")

    # Подтверждение callback query
    await bot.answer_callback_query(callback_query.id)

# # Admin BackupDB
# @dp.callback_query(lambda c: c.data == 'backup')
# async def process_sub_admin_stat(callback_query: types.CallbackQuery):
#     confirmation = backup_db() # - резервная копия
#     if confirmation is True:
#         await bot.send_message(callback_query.from_user.id, "Резервная копия базы данных создана успешно и представленна ниже. Сохранены 3 последние версии в рабочей папке, остальные удалены.")
#     else:
#         await bot.send_message(callback_query.from_user.id, "Ошибка создания резервной копии базы данных.")

#     await asyncio.sleep(0.5)

#     data_folder = Path("./backup_db/")

#     files = [entry for entry in data_folder.iterdir() if entry.is_file()] # Получаем список всех файлов в директории

#     sorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True) # Сортируем список файлов по дате изменения (от новых к старым)

#     for file_to_delete in sorted_files[3:]: # Оставляем последние 3 файла, удаляем остальные
#         os.remove(file_to_delete)
#     logging.info("Remove all file DB, saved 3 latest files.")

#     last_downloaded_file = sorted_files[0] if sorted_files else None   # Последний скачанный файл будет первым в отсортированном списке (новейшим) (адрес)
#     logging.info("Download last DB file.")

#     await bot.send_document(chat_id=callback_query.from_user.id, document=types.input_file.FSInputFile(last_downloaded_file))
#     await bot.answer_callback_query(callback_query.id)





#
# Admin Restore DB
#
# Нажимаю кнопку восстановления, прикрепляю свой файл db бинарный в .sql, он загружается в папку download_db.
# Далее скрипт останавливает все запросы и очищает память, выставляется глобальный флаг, который не допускает  
# пользователям взаимодействовать с базой. Тем временем, очищается полностью и даже разметка работающей базы 
# и полностью переписывается с закаченного файла. Он не удаляется из папки, не думаю что их будет много.
#
 
class Restor_db(StatesGroup):
    load_db = State()
    #restor_db = State()

# Push button - restore
@dp.callback_query(lambda c: c.data == 'restore_db')
async def process_sub_admin_stat(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text="Прикрепи и отправь нужную копию базы данных для восстановления.", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Restor_db.load_db) # Next Step
    await bot.answer_callback_query(callback_query.id) # End typing

# Next step - download db and restore
@dp.message(Restor_db.load_db)
#async def student_name(message: Message, state: FSMContext):
async def load_a_base(message: Message, state: FSMContext):
    global work_in_progress
    work_in_progress = True # Блокировка обращений к базе данных всех пользователей


    if not isinstance(message.document, types.Document):
        await message.answer("Вы передали не документ.")
        return

    file_extension = message.document.file_name.split('.')[-1]
    allowed_extensions = ['sql']

    if file_extension not in allowed_extensions:
        await message.answer("Вы передали файл не sql расширения.")
        return    


    # Name file
    date_time = datetime.datetime.utcnow() # Current date and time
    formtime = date_time.strftime("%Y-%m-%d-%H-%M")
    file_name = f"uploaded-db-{formtime}.sql"

    # await asyncio.sleep(0.3)

    file_path = f"./download_db/{file_name}"
    await bot.download(message.document, file_path) # То что прикрепили и отправили, скачивается в папку с новым именем

    await bot.session.close()
    await dp.storage.close()

    confirmation = restore_db(file_path) # Восстановелние базы

    work_in_progress = False # Восстановление возможности обращения пользователей к базе

    if confirmation == True:
        await message.answer("Восстановление базы данных прошло успешно.")
    else:
        await message.answer("При восстановлении базы данных, что то пошло не так.")


    await state.clear()
    #await state.set_state(Restor_db.restor_db) # Переход к следующему шагу






#### WORK MENU ####
# Main menu strat
@dp.message(Command('setup', 'menu', 'setings'))
async def start(message: types.Message):
    await main_menu(bot, message)
    #await bot.answer_callback_query(callback_query.id)

# Back to main
@dp.callback_query(lambda c: c.data == 'back_to_main')
async def process_back_to_main(callback_query: types.CallbackQuery):
    await back_to_main(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Close menu
@dp.callback_query(lambda c: c.data == 'close')
async def close_main(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=chat_id, message_id=message_id) # Удалить и меню и сообщение
    await bot.answer_callback_query(callback_query.id)
####

#### SETTINGS #### 
# Settings
@dp.callback_query(lambda c: c.data == 'sub_setings')
async def process_sub_setings(callback_query: types.CallbackQuery):
    #await callback_query.answer("Нажали кнопку ") # Выводит уведомление быстрое
    await sub_setings(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Back to Settings
@dp.callback_query(lambda c: c.data == 'back_to_setings')
async def process_back_to_settings(callback_query: types.CallbackQuery):
    await back_to_setings(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)
####

# Settings - model
@dp.callback_query(lambda c: c.data == 'model')
async def process_sub_settings_modell(callback_query: types.CallbackQuery):
    await sub_setings_model(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# @dp.message(Command("model"))
# async def model_command_r(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     print("model")
#     await process_sub_settings_modell(callback_query.message.chat.id)







# Settings - model - gpt-4o-mini
@dp.callback_query(lambda c: c.data == 'gpt-4o-mini')
async def process_sub_settings_modell_gpt_4o_mini(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"set_model": "gpt-4o-mini-2024-07-18"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-4o-mini")
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-4o
@dp.callback_query(lambda c: c.data == 'gpt-4o')
async def process_sub_settings_modell_gpt_4o(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"set_model": "gpt-4o-2024-05-13"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-4o")
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-4-1106-preview
@dp.callback_query(lambda c: c.data == 'gpt-4-1106-preview')
async def process_sub_settings_modell_1106(callback_query: types.CallbackQuery):
    # chat_id = callback_query.message.chat.id
    # message_id = callback_query.message.message_id
    # await bot.send_chat_action(chat_id, action='typing')
    id = user_id(callback_query)
    # await bot.send_chat_action(chat_id, action='typing')
    updated_data = {"set_model": "gpt-4-1106-preview"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-4-1106-preview")
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-4-0125-preview
@dp.callback_query(lambda c: c.data == 'gpt-4-0125-preview')
async def process_sub_settings_modell_0125(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"set_model": "gpt-4-0125-preview"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-4-0125-preview")
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-3.5-turbo-0613
@dp.callback_query(lambda c: c.data == 'gpt-3.5-turbo-0613')
async def process_sub_settings_modell_0125(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"set_model": "gpt-3.5-turbo-0613"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-3.5-turbo-0613")
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-3.5-turbo-0125
@dp.callback_query(lambda c: c.data == 'gpt-3.5-turbo-0125')
async def process_sub_settings_modell_gpt_3_5_turbo_0125(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"set_model": "gpt-3.5-turbo-0125"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-3.5-turbo-0125")
    await bot.answer_callback_query(callback_query.id)  
####

# Settings - time
@dp.callback_query(lambda c: c.data == 'time')
async def process_sub_settings_time(callback_query: types.CallbackQuery):
    await sub_setings_time(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - time - no
@dp.callback_query(lambda c: c.data == 'no_time')
async def process_sub_settings_time_no(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("Каждый вопрос для ChatGPT будет новым.")
    await bot.answer_callback_query(callback_query.id)

# Settings - time - 5 min
@dp.callback_query(lambda c: c.data == '5_time')
async def process_sub_settings_time_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0.05}
    await update_settings(id, updated_data)
    await callback_query.answer("Диалог будет актуальным в течении 5 минут.")
    await bot.answer_callback_query(callback_query.id)

# Settings - time - 15 min
@dp.callback_query(lambda c: c.data == '15_time')
async def process_sub_settings_time_15(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0.15}
    await update_settings(id, updated_data)
    await callback_query.answer("Диалог будет актуальным в течении 15 минут.")
    await bot.answer_callback_query(callback_query.id)

# Settings - time - 30 min
@dp.callback_query(lambda c: c.data == '30_time')
async def process_sub_settings_time_30(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0.30}
    await update_settings(id, updated_data)
    await callback_query.answer("Диалог будет актуальным в течении 30 минут.")
    await bot.answer_callback_query(callback_query.id)
####

# Settings - Creativ
@dp.callback_query(lambda c: c.data == 'creativ')
async def process_sub_settings_creativ(callback_query: types.CallbackQuery):
    await sub_setings_creativ(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - no
@dp.callback_query(lambda c: c.data == 'creativ_0')
async def process_sub_settings_creativ_0(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("100% консервативности в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_3
@dp.callback_query(lambda c: c.data == 'creativ_3')
async def process_sub_settings_creativ_3(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0.3}
    await update_settings(id, updated_data)
    await callback_query.answer("Консервативность 70%, Разнообразие 30%")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_5
@dp.callback_query(lambda c: c.data == 'creativ_5')
async def process_sub_settings_creativ_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0.5}
    await update_settings(id, updated_data)
    await callback_query.answer("Консервативность 50%, Разнообразие 50%")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_7
@dp.callback_query(lambda c: c.data == 'creativ_7')
async def process_sub_settings_creativ_7(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0.7}
    await update_settings(id, updated_data)
    await callback_query.answer("Консервативность 30%, Разнообразие 70%")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_1
@dp.callback_query(lambda c: c.data == 'creativ_1')
async def process_sub_settings_creativ_1(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 1}
    await update_settings(id, updated_data)
    await callback_query.answer("100% Разнообразия в ответах.")
    await bot.answer_callback_query(callback_query.id)
####
    

# Settings - repet
@dp.callback_query(lambda c: c.data == 'repet')
async def process_sub_settings_repet(callback_query: types.CallbackQuery):
    await sub_setings_repet(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - no
@dp.callback_query(lambda c: c.data == 'repet_0')
async def process_sub_settings_repet_0(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("Минимальное повторение в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 3
@dp.callback_query(lambda c: c.data == 'repet_3')
async def process_sub_settings_repet_3(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0.3}
    await update_settings(id, updated_data)
    await callback_query.answer("На 30% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 5
@dp.callback_query(lambda c: c.data == 'repet_5')
async def process_sub_settings_repet_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0.5}
    await update_settings(id, updated_data)
    await callback_query.answer("На 50% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 7
@dp.callback_query(lambda c: c.data == 'repet_7')
async def process_sub_settings_repet_7(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0.7}
    await update_settings(id, updated_data)
    await callback_query.answer("На 70% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 1
@dp.callback_query(lambda c: c.data == 'repet_1')
async def process_sub_settings_repet_1(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 1}
    await update_settings(id, updated_data)
    await callback_query.answer("На 100% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)
####


# Settings - presence
@dp.callback_query(lambda c: c.data == 'repet_all')
async def process_sub_settings_repet_all(callback_query: types.CallbackQuery):
    await sub_setings_repet_all(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - no
@dp.callback_query(lambda c: c.data == 'repet_all_0')
async def process_sub_settings_repet_all_0(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("Минимальное повторение в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 3
@dp.callback_query(lambda c: c.data == 'repet_all_3')
async def process_sub_settings_repet_all_3(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0.3}
    await update_settings(id, updated_data)
    await callback_query.answer("На 30% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 5
@dp.callback_query(lambda c: c.data == 'repet_all_5')
async def process_sub_settings_repet_all_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0.5}
    await update_settings(id, updated_data)
    await callback_query.answer("На 50% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 7
@dp.callback_query(lambda c: c.data == 'repet_all_7')
async def process_sub_settings_repet_all_7(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0.7}
    await update_settings(id, updated_data)
    await callback_query.answer("На 70% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 1
@dp.callback_query(lambda c: c.data == 'repet_all_1')
async def process_sub_settings_repet_all_1(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 1}
    await update_settings(id, updated_data)
    await callback_query.answer("На 100% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)
####


# Settings - flag_stik
@dp.callback_query(lambda c: c.data == 'flag_stik')
async def process_sub_settings_flag_stik(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    data = await get_settings(id)
    if data:
        flag_stik = data['flag_stik']
    if flag_stik == True:
        updated_data = {"flag_stik": False}
        await update_settings(id, updated_data)
        await callback_query.answer("Строка статистики в ответе отключена.")
    if flag_stik == False:
        updated_data = {"flag_stik": True}
        await update_settings(id, updated_data)
        await callback_query.answer("Строка статистики в ответе включена.")
        await bot.answer_callback_query(callback_query.id)
####



# Settings - reset dialog


# Обработчик для callback query
# @dp.message(Command("sub_dialog"))
# async def process_sub_dialog_eer(message: types.Message):
#     await message.reply("Команда /sub_dialog получена")

@dp.callback_query(lambda c: c.data == 'sub_dialog')
async def process_sub_dialog(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"discus": None}
    await update_discussion(id, updated_data)
    await callback_query.answer("Ваш диалог с ChatGPT сброшен.")
    await bot.answer_callback_query(callback_query.id)

####

# Settings - finansi
@dp.callback_query(lambda c: c.data == 'sub_balance')
async def process_sub_balance(callback_query: types.CallbackQuery):
    await sub_balance(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)
####

# Settings - my_many
@dp.callback_query(lambda c: c.data == 'my_many')
async def process_sub_settings_my_many(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    data = await get_settings(id)
    if data:
        money = round(data['money'], 2)
        await bot.send_message(callback_query.from_user.id, f"<b>На вашем счету:\n{money}</b> RUB\n", parse_mode="HTML")
    await bot.answer_callback_query(callback_query.id)
####


#### ADD MONEY ####


# Settings - add_money  Вызывает список вариантов оплат
@dp.callback_query(lambda c: c.data == 'add_money')
async def process_sub_settings_add_money(callback_query: types.CallbackQuery):
    await sub_add_money(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)












#### СНОВНАЯ ФОРМА ОПЛАТЫ ####
# Set State
class Form_my_pay(StatesGroup):
    add_summ = State()
    #confirm_summt = State()



# Запуск цепочки
@dp.callback_query(lambda c: c.data == 'pay_by_card')
async def start_invoice(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения в RUB:\nEnter the deposit amount in RUB:", reply_markup=ReplyKeyboardRemove()) # !!!!
    await bot.answer_callback_query(callback_query.id) # Закрытие сесси кнопки
    await state.set_state(Form_my_pay.add_summ) # Ожидание следующего шага



# Ожидание получения суммы пополнения
@dp.message(Form_my_pay.add_summ, F.content_type.in_({'text'}))
async def invoice_user_1(message: Message, state: FSMContext):

    mes_id = message.chat.id
    summ = message.text
    id = user_id(message)
    admin_id = admin_user_ids[1:-1]
    url = f"tg://user?id={id}"

    # Проверка на число
    if message.text.isdigit() is not True:
        await bot.send_message(message.chat.id, f"Введите только сумму цифрами в RUB.\nEnter only the amount in numbers in RUB.")
        return

    if float(summ) < 50:
        await bot.send_message(message.chat.id, f"Минимальная сумма 50 RUB.\nThe minimum amount is 50 RUB.")
        return

    # запускаю функцию и передаю данные для подтверждения админом.
    await confirm_my_pyz(id, summ, admin_id, mes_id, url)

    # Закрытие Stats
    await state.clear()



# Вызов у админа кнопки подтверждения
async def confirm_my_pyz(id, summ, admin_id, mes_id, url):
    # Кнопка подтверждения
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👛 Подтвердить", callback_data=f"confirm_summ_user_d:{id}:{summ}:{admin_id}:{mes_id}")], 
        ]
    )
    await bot.send_message(admin_id, f"Пользователь: <a href='{url}'>{id}</a>, хочет пополнить счет на: {summ} РУБ", parse_mode="HTML", reply_markup=keyboard)
    await bot.send_message(mes_id, f"Запрос принят, ожидайте.\nThe request has been accepted, wait.")
    return




# Обработчик подтверждения
@dp.callback_query(lambda c: c.data and c.data.startswith('confirm_summ_user_d'))
async def confirm_callback_handler_d(callback_query: types.CallbackQuery):
    data = callback_query.data.split(':')
    if len(data) == 5:
        id = int(data[1])
        summ = float(data[2])
        admin_id = int(data[3])
        mes_id = int(data[4])
    else:
        await bot.answer_callback_query(callback_query.id, text="Ошибка в данных запроса.", show_alert=True)
        return

    data_set = await get_settings(id)
    new_money = data_set.money + float(summ)

    updated_data = {"money": new_money}
    conf = await update_settings(id, updated_data)

    if conf is True:
        await bot.send_message(admin_id, f"Счет клиента {id} пополнен, общий:  {new_money} RUB.")
        await bot.send_message(mes_id, f"Ваш счет пополнен на {summ} RUB\nYour account has been topped up with {summ} RUB.")
        await bot.answer_callback_query(callback_query.id)
        return
    else:
        await bot.send_message(admin_id, f"Ошибка пополнения счета.")
        await bot.answer_callback_query(callback_query.id)
        return
####













# Pay WALLET PAY - че то меня отключили, теперь какие то звезды
        
# State
# class Form_Wallet(StatesGroup):
#     add_wallet = State()
#     confirm_walet = State()

# # Initialize the async API client
# api_walet = AsyncWalletPayAPI(api_key=wallet_pay_token)

# # Нажатие на кнопку оплаты Wallet Pay
# @dp.callback_query(lambda c: c.data == 'wallet_pay')
# async def process_sub_settings_add_money_wallet_pay(callback_query: types.CallbackQuery, state: FSMContext):

#     # Проверка на технические работы
#     if work_in_progress == True:
#         await worc_in_progress(callback_query)
#         return

#     await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения в RUB:", reply_markup=ReplyKeyboardRemove()) # !!!!
    
#     # Закрытие сесси кнопки
#     await bot.answer_callback_query(callback_query.id)

#     # Ожидание следующего шага
#     await state.set_state(Form_Wallet.add_wallet)


# # Ввожу сумму в RUB
# @dp.message(Form_Wallet.add_wallet, F.content_type.in_({'text'}))
# async def invoice_user(message: Message, state: FSMContext):
#     # Проверка что цифры
#     if message.text.isdigit() is not True:
#         await bot.send_message(message.chat.id, f"Введите только сумму цифрами.")
#         return

#     # Сбор данных
#     id = user_id(message)
#     wallet_uuid = str(uuid.uuid4())
#     description_wallet_pay = "Пополнение баланса"
#     summ = message.text
#     currency = "RUB"
#     time_sesion = 60 * 60 * 1 # Час

#     # Create an order
#     order = await api_walet.create_order(
#         amount=summ,
#         currency_code = currency,
#         description = description_wallet_pay,
#         external_id = wallet_uuid, # ID счета на оплату в вашем боте
#         timeout_seconds = time_sesion, # время действия счета в секундах
#         customer_telegram_user_id = id # ID аккаунта Telegram покупателя
#     )

#     # Формирование данных передаваемых на следующий шаг по state
#     await state.update_data(currency=currency, wallet_uuid=wallet_uuid, summ=summ, id=id, order=order )


#     # Формирование ссылки кнопки на оплату
#     payLink = f"https://t.me/wallet/start?startapp=wpay_order-orderId__{order.id}&startApp=wpay_order-orderId__{order.id}"

#     # Кнопка оплаты
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="👛 Pay via Wallet", url=payLink)], 

#         ]
#     )
#     await bot.send_message(message.chat.id, f"Пополнить счет на {summ} {currency} через WALLET PAY:", reply_markup=keyboard)

#     await asyncio.sleep(10)

#     # # Кнопка проверки оплаты Wallet Pay
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="🔍 Проверить и зачислить", callback_data="confirm_summ_wallet")], 

#         ]
#     )
#     await message.answer("После оплаты, подтвердите ваш платеж: ", reply_markup=keyboard)

#     # Ожидание следующего шага
#     await state.set_state(Form_Wallet.confirm_walet)




# #  Нажатие кнопки проверки оплаты оплаты Wallet Pay
# @dp.callback_query(Form_Wallet.confirm_walet, lambda c: c.data == 'confirm_summ_wallet')
# async def process_sub_settings_add_confirm(callback_query: types.CallbackQuery, state: FSMContext):

#     # Проверка на технические работы
#     if work_in_progress == True:
#         await worc_in_progress(callback_query)
#         return

#     # Получение данных из state
#     data = await state.get_data()
#     order = data.get('order')
#     currency = data.get('currency')
#     wallet_uuid = data.get('wallet_uuid')
#     summ = data.get('summ')
#     id = data.get('id')
    
#     #Get order list
#     #orders = await api_walet.get_order_list(offset=0, count=10)
#     # Get order amount  Получить сумму заказа
#     # amount = await api_walet.get_order_amount()
#      # Get order preview
#     order_preview = await api_walet.get_order_preview(order_id=order.id)


#     # Check if the order is paid
#     if order_preview.status == "PAID":
#         await add_money_wallet_pay(data)
#         await bot.send_message(callback_query.from_user.id, f"Ваш платеж подтвержден:\nОплачено: *{summ} {currency}*,\nКомиссия на нас,\nЗачисленно: *{summ} {currency}*.")
#         logging.info(f"Order has been paid! user.id: {id}, order.id: {order.id}, order.status: {order.status}, order.number: {order.number}, wallet_uuid: {wallet_uuid}, summ: {summ}, currency: {currency}")
#         await bot.answer_callback_query(callback_query.id)
#         await state.clear()
#         return
#     else:
#         await bot.send_message(callback_query.from_user.id, "Оплата не найдена, попробуйте позже.")
#         logging.info("Order is not paid yet")
#         await asyncio.sleep(5)
#         await bot.answer_callback_query(callback_query.id)




# Pay cripto
        
# State
class Form_transfer(StatesGroup):
    start_cripto = State()
    name_cripto = State()
    summ_cripto = State()
    confirm_cripto = State()

# Нажатие на кнопку оплаты cripto
@dp.callback_query(lambda c: c.data == 'cripto')
async def process_add_cripto(callback_query: types.CallbackQuery, state: FSMContext):

    #Кнопка подтверждение оплаты cripto
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Подтвердить перевод", callback_data="confirm_cripto")], 

        ]
    )
    await bot.send_message(callback_query.from_user.id, f"*USDT*: TMsUumKvMScNwxEhLEWjuxR2c1BUQXBPgf\n*Сеть*: TRC20\n\n*BTC*: 1CpxUycn3bEMvH8873FYv8JxUpdiXKArS4\n", reply_markup=keyboard) # !!!!
    # Закрытие сесси кнопки
    await bot.answer_callback_query(callback_query.id)
    # Ожидание следующего шага
    await state.set_state(Form_transfer.start_cripto)

#  Нажатие кнопки подтверждение оплаты cripto
@dp.callback_query(Form_transfer.start_cripto)
async def process_sub_start_cripto(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, f"Введите название переводимой вами криптовалюты:", reply_markup=ReplyKeyboardRemove()) # !!!!
    # Закрытие сесси кнопки
    await bot.answer_callback_query(callback_query.id)
    # Ожидание следующего шага
    await state.set_state(Form_transfer.summ_cripto)

#  Ввод валюты
@dp.message(Form_transfer.summ_cripto, F.content_type.in_({'text'}))
async def process_sub_name_cripto(message: Message, state: FSMContext):
    # Проверка что цифры
    if message.text.isdigit() is True:
        await bot.send_message(message.chat.id, f"Введите название, а не сумму.")
        return
    # Формирование данных передаваемых на следующий шаг по state
    await state.update_data(name_cripto=message.text)
    await bot.send_message(message.chat.id, f"Введите сумму переводимой вами криптовалюты:", reply_markup=ReplyKeyboardRemove())
    # Ожидание следующего шага
    await state.set_state(Form_transfer.confirm_cripto)

#  Ввод суммы
@dp.message(Form_transfer.confirm_cripto, F.content_type.in_({'text'}))
async def process_sub_summ_cripto(message: Message, state: FSMContext):
    
    # Проверка что цифры
    if message.text.isdigit() is not True:
        await bot.send_message(message.chat.id, f"Введите сумму, а не сумму.")
        return
    # Подготовка данных
    id = user_id(message)
    # С прошлого State
    data = await state.get_data()
    currency = data.get('name_cripto')

    data = await state.update_data(name_summ=message.text, id=id, currency=currency)
    # Функция по добавлению в базу
    await add_money_cripto(data)
    await bot.send_message(message.chat.id, f"После проверки оплаты, ваш баланс пополнится.\n\n Пожалуйста, производите таким методом одну оплату, следующую после подтверждения прошлой.\n\n Для ускорения процесса, просьба скинуть подтверждение @Shliamb\n\n Ожидайте пожалуйста.")
    await state.clear()



# Settings - satatistic for 100
@dp.callback_query(lambda c: c.data == 'statis_30')
async def process_sub_settings_statis_30(callback_query: types.CallbackQuery):
    id = user_id(callback_query)

    name = callback_query.from_user.username
    full_name = callback_query.from_user.full_name
    first_name = callback_query.from_user.first_name
    last_name = callback_query.from_user.last_name
    if name is not None:
        about = name
    elif full_name is not None:
        about = full_name
    elif first_name is not None:
        about = first_name
    elif last_name is not None:
        about = last_name

    chat_id = callback_query.message.chat.id
    # message_id = callback_query.message.message_id

    data = await get_last_30_statistics(id)
    all_static = []
    all_static.append(["№", "Имя" , "Время", "Модель", "Токенов в сесии",
                        "Цена 1 токена RUB", "Общая цена сесии RUB"]) # First a names row
    if data:
        for statistic in data:
            namba_id = statistic.id
            time_d = statistic.time
            use_model = statistic.use_model
            sesion_token = statistic.sesion_token
            price_1_tok = round(statistic.price_1_tok,8)
            price_sesion_tok = round(statistic.price_sesion_tok, 5)
            # users_telegram_id = statistic.users_telegram_id # Обычные люди при виде id вспомнят РЕНтв)))
            all_static.append([namba_id, about, time_d, use_model, sesion_token, price_1_tok, price_sesion_tok]) # added user data


    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()

    # csv file to download
    file_name = f"Stat-{datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=chat_id, document=buffered_input_file)
        await bot.answer_callback_query(callback_query.id)
    except:
        print(f"Error sending document Statistic 100 point of Users")
####




# Settings - terms
@dp.callback_query(lambda c: c.data == 'terms')
async def process_sub_terms(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, terms, parse_mode="HTML")
    await bot.answer_callback_query(callback_query.id)



# Settings - about
@dp.callback_query(lambda c: c.data == 'sub_about')
async def process_sub_about(callback_query: types.CallbackQuery):
    #await sub_about(bot, callback_query)
    await bot.send_message(callback_query.from_user.id, about_text, parse_mode="HTML") # about_bot.py
    await bot.answer_callback_query(callback_query.id)





#### OpenAI ####
#second_function_finished = False # Флаг для отслеживания статуса второй функции.

# Typing in OpenAI
# async def first_function(message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     await asyncio.sleep(5)


# @dp.message(F.content_type.in_({'text', 'sticker'})) # Только текст и зачем то стикеры..
# async def start_main(message):



# Answer OpenAI
@dp.message(F.content_type.in_({'text', 'sticker'}))
async def second_function(message: types.Message):
    await typing(message)

    id = user_id(message)
    logging.info(f"User {id} - {message.text}")

    if message.text is None or message.text.startswith('/') or not isinstance(message.text, str):
        await message.answer("Извините, сообщение в неподдерживаемом формате.\nSorry, the message is in an unsupported format.")
        logging.error(f"Error, not correct message from User whose id is {id}")
        return

    data = await get_settings(id)  # Получаем настройки
    if data is None:
        await command_start_handler(message)
        logging.info(f"User {id} is not on DB, added.")
        return

    if str(id) in block:
        await message.answer("Извините, но вы заблокированы, попробуйте обратиться к @Shliamb.\nSorry, but you are blocked, try contacting @Shliamb.")
        logging.info(f"The user id:{id} blocked and typing question.")
        return

    # Получение всех необходимых данных пользователя
    temp_chat = data['temp_chat']
    frequency = data['frequency']
    presence = data['presence']
    all_count = data['all_count']
    all_token = data['all_token']
    the_gap = data['the_gap']
    set_model = data['set_model']
    give_me_money = data['give_me_money']
    money = data['money']
    all_in_money = data['all_in_money']
    flag_stik = data['flag_stik']  # Флаг для стикера

    if money < 0 or money == 0:
        await message.answer("Извините, но похоже, у вас нулевой баланс. Пополнить - [/setup]\nSorry, but it looks like you have a zero balance. Top up - [/setup]")
        logging.info(f"User {id} has finished their money.")
        return

    cache = []
    ged = await get_discussion(id)
    if ged is not None:
        discus = ged.get('discus')  # Используем .get() для безопасного извлечения
        date_db = ged.get('timestamp')  # Время из базы записи

    if date_db:  # Проверяем, что timestamp не равен None
        day_db = date_db.strftime("%Y-%m-%d")
        time_db = date_db.strftime("%H.%M")

        now = get_time()
        date_now = now['day']
        time_now = now['time']

        difference = float(time_now) - float(time_db)  # Разница

        if day_db == date_now and difference < the_gap and discus is not None:
            cache.append(discus)
    else:
        logging.error("Timestamp (date_db) is None, skipping strftime.")

    # Формируем запрос к OpenAI
    cache.append(f"{message.text}\n")
    format_session_data = ' '.join(cache)

    try:
        answer = await client.chat.completions.create(
            messages=[{"role": "user", "content": format_session_data}],
            model=set_model,
            temperature=temp_chat,
            frequency_penalty=frequency,
            presence_penalty=presence
        )
    except RateLimitError as e:
        admin_id = admin_user_ids[1:-1]
        error_message = str(e)
        error_code_match = re.search(r"Error code: (\d+)", error_message)
        error_code = error_code_match.group(1) if error_code_match else "No code provided"
        print(f"Ошибка {error_code}: {error_message}")
        if error_code == '429':
            await bot.send_message(admin_id, f"На сервере OpenAI отрицательный счет, пополните пожалуйста.")
            await bot.send_message(message.chat.id, "RU: Извините, на общем счете OpenAI отрицательный счет, в ближайшее время администратор пополнит его.\n\nEn: Sorry, there is a negative account on the general OpenAI account, the administrator will replenish it in the near future.")
        return
    
    except OpenAIError as e:
        # Обработка других ошибок OpenAI
        error_message = str(e)
        print(f"Произошла ошибка: {error_message}")
        return

    if answer is not None:
        ######### This date from Open AI ########
        text = answer.choices[0].message.content  # Text response AI
        model_version = answer.model  # Model in answer
        used_tokens = answer.usage.total_tokens 
        ######### This date from Open AI ########

    # Рассчитываем расход
    data = {
        "id": id,
        "model_version": model_version,
        "used_tokens": used_tokens,
        "all_count": all_count,
        "all_token": all_token,
        "give_me_money": give_me_money,
        "money": money,
        "all_in_money": all_in_money,
    }

    rashod = await calculation(data)

    # Показать статистику в ответе
    stik = f"\nмодель:{model_version}\nисп.:{used_tokens}ток.\nрасх.:{round(rashod, 2)}RUB  [/setup]" if flag_stik else ""
    send = f"{text}\n\n{stik}"
    await message.answer(send)
 

    # Обновляем информацию в базе данных
    cache.append(f"{text}\n")
    clear_data = ' '.join(cache)

    updated_data = {
        "discus": clear_data,
        # "timestamp": timestamp,  # Возможно, нужно добавить timestamp, если это необходимо
    }

    await update_discussion(id, updated_data)
    cache = []


###VOICE###

@router.message()
async def telegram_message_handler(message: Message, bot):
    logging.info(f"Получено сообщение: {message}")
    if message.voice:
        logging.info(f"Получено голосовое сообщение")
        await handle_voice_message(message, bot)
    else:
        logging.info(f"Получено текстовое сообщение")
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        answer = await ask_gpt(message.text)
        if answer:
            await message.answer(answer, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer("Произошла ошибка при обработке сообщения.", parse_mode=ParseMode.MARKDOWN)

# Путь к папке для хранения временных файлов
TEMP_FOLDER = '/Users/urgan67/Desktop/bot/voice'

# Убедитесь, что папка существует
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

async def stt(file_path):
    async with aiofiles.open(file_path, 'rb') as audio_file:
        transcription = await openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription['text']

async def handle_voice_message(message, bot):
    chat_id = str(message.chat.id)
    unique_name = str(int(time.time()))
    
    # Указываем путь для сохранения файла в папке TEMP_FOLDER
    save_path = os.path.join(TEMP_FOLDER, f'{unique_name}.ogg')
    
    # Убедитесь, что файл ошибки существует по правильному пути
    error_audio_path = '/Users/urgan67/Desktop/bot/error_audio.ogg'  # Укажите верный путь

    # Получаем файл и скачиваем его
    file_id = message.voice.file_id
    file = await bot.get_file(file_id=file_id)
    await bot.download_file(file.file_path, save_path)

    try:
        # Преобразуем речь в текст
        speech_text = await stt(save_path)
        if not speech_text:
            if os.path.exists(error_audio_path):
                await bot.send_voice(chat_id=chat_id, voice=FSInputFile(error_audio_path))
            else:
                logging.error(f"Файл ошибки {error_audio_path} не найден.")
            return
    except Exception as e:
        logging.error(f"Ошибка при преобразовании речи: {e}")
        if os.path.exists(error_audio_path):
            await bot.send_voice(chat_id=chat_id, voice=FSInputFile(error_audio_path))
        else:
            logging.error(f"Файл ошибки {error_audio_path} не найден.")
        return

    # Оповещаем, что бот "печатает" ответ
    await bot.send_chat_action(chat_id=chat_id, action="typing")

    # Отправляем текст на GPT и получаем ответ
    gpt_answer = await ask_gpt(speech_text)
    if not gpt_answer:
        await bot.send_voice(chat_id=chat_id, voice=FSInputFile(error_audio_path))
        return

    # Преобразуем текст ответа в голос
    response_audio_path = os.path.join(TEMP_FOLDER, f'response_{unique_name}.ogg')
    await tts(gpt_answer, response_audio_path)

    # Сохраняем аудио файл в папке TEMP_FOLDER
    audio_file = FSInputFile(response_audio_path)
    
    # Отправляем аудио обратно пользователю
    response_message = await bot.send_voice(chat_id=chat_id, voice=audio_file)

    # Удаляем исходное голосовое сообщение
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    # Удаляем временные файлы, сохранённые в папке
    os.remove(save_path)  # Удаляем загруженный файл
    os.remove(response_audio_path)  # Удаляем отправленный ответ

async def ask_gpt(text):
    # Отправка текста в GPT и получение ответа
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "user", "content": text},
        ]
    )
    return response['choices'][0]['message']['content']

async def tts(text, file_path):
    # Преобразование текста в речь и сохранение в файл
    tts = gTTS(text=text, lang='ru')
    await asyncio.get_event_loop().run_in_executor(None, tts.save, file_path)
    logging.info(f"TTS файл сохранен как {file_path}")

# # Закрытие клиентских сессий
# async def close_sessions():
#     await bot.session.close()




# async def main_ai(message):
#     # Запускаем вторую функцию и сохраняем Task объект.
#     second_task = asyncio.create_task(second_function(message))
    
#     # Цикл для периодического запуска первой функции каждые 5 секунд до завершения второй функции.
#     while not second_task.done():
#         await first_function(message)
#         await asyncio.sleep(1)  # Ожидаем небольшое время перед следующей проверкой.




# Start Message to OpenAI
# @dp.message(F.content_type.in_({'text', 'sticker'})) # Только текст и зачем то стикеры..
# async def start_main(message):
#     await main_ai(message)






# Main polling
# async def backup_loop(): # Запуск таски на бекап 
#     while True:
#         task_backup.schedule.run_pending()
#         await asyncio.sleep(1)


async def main_bot() -> None:
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    


# Start and Restart
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # retries = 5
    # while retries > 0:
    try:
        asyncio.run(main_bot())
        #break # Если выполнение успешно - выходим из цикла.
    except Exception as e:
        logging.error(f"An error occurred: {e}. Restarting after a delay...")
        # retries -= 1
        
        # if retries > 0:
        #     time.sleep(5)  # Ожидаем перед попыткой перезапуска
