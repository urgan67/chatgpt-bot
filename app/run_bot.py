import logging

# logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
# logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл

from keys import (
    token, api_key, white_list, admin_user_ids,
    #, receiver_yoomoney, token_yoomoney, wallet_pay_token
                   )
# from about_bot import about_text
# from terms_of_use import terms
import time
import sys
import re
import os
import asyncio
from pathlib import Path
from openai import OpenAIError, AsyncOpenAI, RateLimitError
from aiogram import Bot, Dispatcher, types, F, Router
# from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import csv
import datetime
from io import StringIO, BytesIO
# from get_time import get_time
# from calculation import calculation
# from backupdb import backup_db
# from restore_db import restore_db
# from add_money import add_money_by_card, add_money_wallet_pay, add_money_cripto
#import task_backup
#from yoomoney import Quickpay
# from yoomoney import Client
# from WalletPay import AsyncWalletPayAPI
# from WalletPay import WalletPayAPI, WebhookManager
# from WalletPay.types import Event
# import uuid
from worker_db import (
    adding_user, get_user_by_id, update_user, add_settings, add_discussion, update_settings,
    get_settings, get_discussion, update_discussion, get_exchange, update_exchange, get_last_30_statistics,
    get_all_stat_admin
)
# from keyboards import (
#     main_menu, sub_setings, sub_balance, back_to_main, back_to_setings,\
#     sub_setings_model, sub_setings_time, sub_setings_creativ, sub_setings_repet, sub_setings_repet_all,\
#     sub_add_money, admin_menu, confirm_summ
# )

# Логирование
logging.basicConfig(level=logging.INFO)

client = AsyncOpenAI(api_key=api_key)
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls



# Флаг технических работ, избегает обращения к базе пользователями, для восстановления базы
# Глобальная переменная для флага технических работ
work_in_progress = False

async def worc_in_progress(goo):
    global work_in_progress

    if work_in_progress:
        # Если ведутся технические работы, отправляем сообщение пользователю
        await goo.answer("Извините, ведутся технические работы, попробуйте через 1 минуту.\nSorry, technical work is underway, try it in 1 minute.")
        logging.info("Tech maintenance in progress, sorry.")
    else:
        # Если нет технических работ, выполняем нужную операцию
        await goo.answer("Operation successful.")
        logging.info("Operation completed successfully.")


# Получение user_id из action
def user_id(action) -> int:
    return action.from_user.id

# Показываем статус "печатает", отправляем действие в Telegram
async def typing(action) -> None:
    try:
        # Отправка статуса "печатает" в чат
        await bot.send_chat_action(action.chat.id, action='typing')
        # Вы можете добавить задержку, если хотите
        # await asyncio.sleep(5)
    except Exception as e:
        logging.error(f"Failed to send typing action: {e}")



# PUSH /START
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    if work_in_progress:
        await worc_in_progress(message)
        return

    # Меню
    bot_commands = [
        BotCommand(command="/menu", description="Главное меню | Main Menu"),
        # BotCommand(command="/sub_dialog", description="Сброс диалога | Resetting the dialog"),
        # BotCommand(command="/model", description="Выбрать модель GPT | Choose a GPT model"),
    ]
    await bot.set_my_commands(bot_commands)

    ###### Get All data user on telegram ######
    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    is_admin = False
    admin_user_ids = [admin_user_ids]  # Пример admin_user_ids
 
    # Логируем
    logging.info(f"User {id} press /start")

    # Preparing data for the user
    user_data = {
        "id": id, 
        "name": name, 
        "full_name": full_name, 
        "first_name": first_name,
        "last_name": last_name, 
        "chat_id": chat_id, 
        "is_admin": is_admin
    }

    # Если пользователь уже существует в базе, обновляем данные, иначе добавляем нового
    try:
        is_on_user = await get_user_by_id(id)
        if is_on_user is not None:
            await update_user(id, user_data)  # Обновление данных пользователя
        else:
            await adding_user(user_data)  # Добавление нового пользователя
            await add_settings(id)  # Добавление настроек
            await add_discussion(id)  # Добавление обсуждений
    except Exception as e:
        logging.error(f"Error during user database operations: {e}")

    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "bro"))

    # Checking and adding the parameters in Settings to white list users and gives them money
    if str(id) in white_list:
        money = 1000  # Yep!
        updated_data = {"money": money}
    
        # Обновляем деньги для пользователя в базе данных
        confirmation = await update_settings(id, updated_data)  # Gives money
        if confirmation:
            logging.info(f"1000 RUB added, user id is: {id}.")
        else:
            logging.error(f"1000 RUB has not been added, user id is: {id}.")

# Send greeting message
    await message.answer(
        f"Привет {about}! Я *ChatGPT*. Мне можно сразу задать вопрос или настроить - /setup. Там же можно выбрать последнюю модель ChatGPT.\n"
        f"Hello {about}! I am *ChatGPT*. You can ask me a question right away or set up - /setup. You can also select the latest ChatGPT model there."
            )
        

async def main_bot() -> None:
    #backup_task = asyncio.create_task(backup_loop())
    await dp.start_polling(bot, skip_updates=False) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей



# Start and Restart
if __name__ == "__main__":
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


    ###### Get All data user on telegram ######
# async def handle_voice_message(message: Message, bot: Bot):
#     chat_id = str(message.chat.id)
#     unique_name = str(int(time.time()))
#     save_path = f'{unique_name}.ogg'

#     # Получаем файл и скачиваем его
#     file_id = message.voice.file_id
#     file = await bot.get_file(file_id=file_id)
#     await bot.download_file(file.file_path, save_path)

#     try:
#         # Преобразуем речь в текст
#         speech_text = await stt(save_path)
#         if not speech_text:
#             await bot.send_voice(chat_id=chat_id, voice=FSInputFile('path_to_error_audio.ogg'))  # Добавьте путь к аудиофайлу ошибки
#             return
#     except Exception as e:
#         await bot.send_voice(chat_id=chat_id, voice=FSInputFile('path_to_error_audio.ogg'))  # Добавьте путь к аудиофайлу ошибки
#         return

#     # Оповещаем, что бот "печатает" ответ
#     await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

#     # Отправляем текст на GPT и получаем ответ
#     gpt_answer = await ask_gpt(speech_text)
#     if not gpt_answer:
#         await bot.send_voice(chat_id=chat_id, voice=FSInputFile('path_to_error_audio.ogg'))  # Добавьте путь к аудиофайлу ошибки
#         return

#     # Преобразуем текст ответа в голос
#     response_audio_path = f'response_{unique_name}.ogg'
#     await tts(gpt_answer, response_audio_path)

#     # Отправляем аудио обратно пользователю
#     audio_file = FSInputFile(response_audio_path)
#     await bot.send_voice(chat_id=chat_id, voice=audio_file)

# async def stt(file_path):
#     with open(file_path, "rb") as audio_file:
#         transcription = openai.Audio.transcribe(
#             model="whisper-1",
#             file=audio_file
#         )
#     return transcription['text']

# async def tts(text, file_path):
#     tts = gTTS(text=text, lang='ru')  # Убедитесь, что язык установлен на 'ru'
#     await asyncio.get_event_loop().run_in_executor(None, tts.save, file_path)
#     logging.info(f"TTS файл сохранен как {file_path}")

# async def ask_gpt(text):
#     response = await asyncio.get_event_loop().run_in_executor(
#         None,
#         lambda: openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "user", "content": text},
#             ]
#         )
#     )
#     return response['choices'][0]['message']['content']

# @router.message()
# async def telegram_message_handler(message: Message, bot: Bot):
#     if message.voice:
#         await handle_voice_message(message, bot)
#     else:
#         # Оповещаем, что бот "печатает" ответ
#         await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
#         answer = await ask_gpt(message.text)
#         if answer:
#             await message.answer(answer, parse_mode=ParseMode.MARKDOWN)
#         else:
#             await message.answer("Произошла ошибка при обработке сообщения.", parse_mode=ParseMode.MARKDOWN)

# async def main() -> None:
#     bot = Bot(token=TOKEN)
#     dp = Dispatcher()
#     dp.include_router(router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
