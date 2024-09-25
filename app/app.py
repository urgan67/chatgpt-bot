from worker import add_data_user, get_data_user




# Добавляем пользователя:
# Сбор данных:
# user_id = 21258098   # !
# name = "Mark"
# cash = 0.0

data = {
    "user_id": 212580111,
    "name": 'Ann',
    "cash": 10,
}
user_id = data.get('user_id')
name = data.get('name')
cash = data.get('cash')
print(user_id, name, cash)

# Запуск функции:
confirm = add_data_user(data)
confirm = get_data_user(21258098)
confirm = get_data_user(212580)
if confirm is True:
    print("Пользователь {user_id} {name} внесен в таблицу users.")
else:
    print("Ошибка записи данных в таблицу Users.")



# # Получаем пользователя:
# user_id = 1258098
# data = get_data_user(user_id)
# print(data)











# add_data_user(user_id, name, cash, dfdfd, dfdfgdfgd, dfdgfdgfd, dffdgdfgf, dfdd)

# 1. data = {} -> add_data_user(data}
# 2. 








