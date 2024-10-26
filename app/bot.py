import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand

from keys import token, white_list
from worker_db import adding_user, get_user_by_id, update_user
from openai_gpt import question_openai
from text_model_openai import price

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

    user = await get_user_by_id(id)
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
    
    text = message.text
   

    data = await get_user_by_id(id) 

    

    if str(id) in white_list:
        flag = True

    money = data.get("money")
    if money <=0 and flag == False:
        await bot.send_message(message.chat.id, "Извините, на счете не достаточно средств")
        return
    
    model = 'gpt-4o-mini-2024-07-18'
    response = await question_openai(text, model)
    await message.answer(response.get("gpt_response"), markdown = 'markdown')
    if flag == True:
        return
    else:
        total_tokens = response.get("total_tokens")
        tok_1_rub = price.get(model) / 1000
        total_coast = total_tokens * tok_1_rub

        new_money = money - total_coast
        new_data = {"user_id": id, "money": new_money}

        confirm = await update_user(new_data)
        if confirm:
            # await bot.send_message(message.chat.id, "Баланс обновлен")
            return
        else:
            await message.answer("При обработке вашего запроса возникла ошибка.")
            return
          

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

