from worker import get_data_user,update_data_user,add_data_user


data = {
    "user_id": 1,
    "name": 'Anny',
    "cash": 15000,
    "session_id": 1,
    "tokens": 10000,
    "price": 2,  
}

# print(data.get("name"))

# confirm = add_data_user(data)
# print(data)

# user_id = 1  # Замените на нужный user_id
# new_cash_value = 100.0  # Замените на нужное значение cash
# result = update_data_user(user_id, new_cash_value)

user_id = 1
confirm = get_data_user(user_id)
print(confirm)