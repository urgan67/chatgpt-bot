from worker import get_data_user,update_data_user,add_data_user


data = {
    "user_id": 11,
    "name": 'фывasfhgjhf',
    "cash": 15000,  
}

# print(data.get("name"))

# confirm = add_data_user(data)
# print(data)

user_id = 11  # Замените на нужный user_id
new_cash_value = 100.0  # Замените на нужное значение cash
result = update_data_user(data)

user_id = 11
confirm = get_data_user(user_id)
print(confirm)