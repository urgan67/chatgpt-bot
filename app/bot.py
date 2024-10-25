import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand

from keys import token, white_list
from worker_db import adding_user, get_user_by_id, update_user
from openai_gpt import question_openai


bot = Bot(token=token)
dp = Dispatcher()


# Получить ID пользователя
def user_id(action) -> int:
    return action.from_user.id

async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')


# Команда /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    # меню
    bot_commands = [
        BotCommand(command="/menu", description="Главное меню | Main Menu"),
    ]
    await bot.set_my_commands(bot_commands)

    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    user_data = {
        "user_id": id,
        "name": name,
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name
    }
    # print(user_data)

    hello = user_data["name"] or user_data["first_name"] or user_data["last_name"] or "bro"

    if str(id) in white_list:
        user_data["money"] = 100
    else:
        user_data["money"] = 30

    user = await get_user_by_id(user_data)
    # print(user)

    # print(user_data)
    if user:
        if str(id) in white_list:
            confirm = await update_user(user_data)
            if confirm:
                await bot.send_message(message.chat.id, "На счете 100р")
        else:
            await bot.send_message(message.chat.id, f"{hello} Вы уже есть в базе данных")            
    else:
        # print("yes")
        confirm_add = await adding_user(user_data)
        print(confirm_add)
        if confirm_add:
            await bot.send_message(message.chat.id, f"Привет {hello}! Я *ChatGPT*. Задайте вопрос или настройте - /setup.")
     
        



@dp.message(F.content_type.in_({'text'}))
async def ask_gpt(message: types.Message):
    await typing(message)

    id = user_id(message)
    flag = False
    model = None
    text = message.text

    price = {                              # при курсе 1$ = 100 руб.
    'gpt-4-turbo': 0.08,               # 7.22 руб.
    'gpt-4-turbo-2024-04-09': 0.08,    # 7.22 руб.
    'tts-1': 0.01,                     # 1 руб.
    'tts-1-1106': 0.01,                # 1 руб.
    'chatgpt-4o-latest': 0.04,         # 4 руб.
    'dall-e-2': 0.08,                  # 7.22 руб.
    'whisper-1': 0.006,                # 0.6 руб.
    'gpt-4-turbo-preview': 0.08,       # 7.22 руб.
    'gpt-3.5-turbo-instruct': 0.005,   # 0.5 руб.
    'gpt-4-0125-preview': 0.08,        # 7.22 руб.
    'gpt-3.5-turbo-0125': 0.004,       # 0.4 руб.
    'gpt-4o-2024-08-06': 0.04,         # 4 руб.
    'gpt-3.5-turbo': 0.0015,           # 0.15 руб.
    'gpt-4o': 0.04,                    # 4 руб.
    'babbage-002': 0.002,              # 0.2 руб.
    'davinci-002': 0.03,               # 3 руб.
    'gpt-4o-realtime-preview-2024-10-01': 0.05,  # 5 руб.
    'dall-e-3': 0.09,                  # 8.13 руб.
    'gpt-4o-realtime-preview': 0.05,   # 5 руб.
    'gpt-4o-mini': 0.0015,             # 0.15 руб.
    'gpt-4o-2024-05-13': 0.04,         # 4 руб.
    'gpt-4o-mini-2024-07-18': 0.0015,  # 0.15 руб.
    'gpt-4o-audio-preview-2024-10-01': 0.02,  # 2 руб.
    'gpt-4o-audio-preview': 0.02,      # 2 руб.
    'tts-1-hd': 0.015,                 # 1.5 руб.
    'tts-1-hd-1106': 0.015,            # 1.5 руб.
    'gpt-4-1106-preview': 0.08,        # 7.22 руб.
    'text-embedding-ada-002': 0.0008,  # 0.08 руб.
    'gpt-3.5-turbo-16k': 0.004,        # 0.4 руб.
    'text-embedding-3-small': 0.0005,  # 0.05 руб.
    'text-embedding-3-large': 0.003,   # 0.3 руб.
    'gpt-3.5-turbo-1106': 0.004,       # 0.4 руб.
    'gpt-4-0613': 0.18,                # 16.24 руб.
    'gpt-4': 0.18,                     # 16.24 руб.
    'gpt-3.5-turbo-instruct-0914': 0.005,  # 0.5 руб.
}


    user_data = {
        "user_id": id,
    }

    data = await get_user_by_id(user_data)

    

    


    if str(id) in white_list:
        flag = True
        
    money = data["money"]

    if money <=0 and flag == False:
        await bot.send_message(message.chat.id, "Извините, на счете не достаточно средств")
        return
    
    try:
        response = await question_openai(text, model)
        if response:
            await message.answer(response.get("gpt_response", 'total_tokens'), markdown = 'markdown')
            if flag == True:
                return
            total_tokens = response["total_tokens"]
            model_used = response["model"]
            tok_1_rub = price.get(model_used, 0) / 1000
            all_token = total_tokens * tok_1_rub

            new_money = money - all_token
            new_data = {"user_id": id, "money": new_money}

            await update_user(new_data)
            await bot.send_message(
                    message.chat.id, 
                    f"Потрачено {total_tokens} токенов. С вашего счета списано {all_token:.2f} руб. Остаток: {new_money:.2f} руб."
                )

            return
        else:
            await message.answer("При обработке вашего запроса возникла ошибка.")
            return
    except Exception as e:
        err = str(e)
        print(f"Произошла ошибка: {err}")
        return








async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

