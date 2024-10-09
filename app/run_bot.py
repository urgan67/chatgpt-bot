import logging
logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
from keys import (
    token, key, white_list, admin_user_ids,
    block, oppas#, receiver_yoomoney, token_yoomoney, wallet_pay_token
    )
# from about_bot import about_text
# from terms_of_use import terms
import time
import sys
import re
import os
import asyncio
import openai
import csv
import datetime

from openai import AsyncOpenAI, RateLimitError, OpenAIError

from aiogram.enums import ParseMode, ChatAction
from aiogram.types import Message, FSInputFile
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from io import StringIO, BytesIO
# from get_time import get_time
# from calculation import calculation
# from backupdb import backup_db
# from restore_db import restore_db
# from add_money import add_money_by_card, add_money_wallet_pay, add_money_cripto

from gtts import gTTS

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


client = openai.api_key = key
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls


# Флаг технических работ, избегает обращения к базе пользователями, для восстановления базы
global work_in_progress
work_in_progress = False
async def worc_in_progress(goo):
    await goo.answer("Извините, ведутся технические работы, попробуйте через 1 минуту.\nSorry, technical work is underway, try it in 1 minute.")
    logging.info(f"Tech maintenance in progress, sorry.")

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

    if work_in_progress == True:
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
    is_admin = False
    admin_id = admin_user_ids[1:-1]
    ###### Get All data user on telegram ######

    logging.info(f"User {id} press /start")

    # Checking and added the parameters
    if str(id) in admin_user_ids:
        is_admin = True
        logging.info(f"The user id:{id} is assigned as an admin.")
   
    # Preparing data for the user
    user_data = {"id": id, "name": name, "full_name": full_name, "first_name":first_name,\
                    "last_name": last_name,"is_admin": is_admin,
                }


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
