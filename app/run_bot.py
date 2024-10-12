import asyncio

from keys import (
    token, api_key, white_list, admin_user_ids)


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
from io import StringIO, BytesIO

from worker_db import (
    adding_user, get_user_by_id, update_user, add_settings, add_discussion, update_settings,
    get_settings, get_discussion, update_discussion, get_exchange, update_exchange, get_last_30_statistics,
    get_all_stat_admin, update_balance
)
# from keyboards import (
#     main_menu, sub_setings, sub_balance, back_to_main, back_to_setings,\
#     sub_setings_model, sub_setings_time, sub_setings_creativ, sub_setings_repet, sub_setings_repet_all,\
#     sub_add_money, admin_menu, confirm_summ
# )
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls


# PUSH /START
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    ###### Get All data user on telegram ######
    user_id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
   
    print(f"User {id} press /start")

    # Preparing data for the user
    user_data = {
        "user_id": user_id, 
        "name": name, 
        "full_name": full_name, 
        "first_name": first_name,
        "last_name": last_name, 
    }
    

    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "bro"))

    # Checking and adding the parameters in Settings to white list users and gives them money
    if str(id) in white_list:
        money = 1000  # Yep!
        updated_data = {"money": money}
    
        # Обновляем деньги для пользователя в базе данных
        confirmation = await update_settings(id, updated_data)  # Gives money
        if confirmation:
            return(f"1000 RUB added, user id is: {id}.")
        else:
            return(f"1000 RUB has not been added, user id is: {id}.")

# Send greeting message
    await message.answer(
        f"Привет {about}! Я *ChatGPT*. Мне можно сразу задать вопрос или настроить - /setup. Там же можно выбрать последнюю модель ChatGPT.\n"
        f"Hello {about}! I am *ChatGPT*. You can ask me a question right away or set up - /setup. You can also select the latest ChatGPT model there."
            )
    

    
    