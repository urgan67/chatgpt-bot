from worker import get_data_user,update_data_user,add_data_user,add_data_session,get_data_session

data = {
    "user_id": 4,
    "name": 'ANTON',
    "cash": 1500,
}

data_session = {
    "user_id": 4,
    "tokens": 10,
    "price": 1,
    # "session_id": 1
}

user_id = data.get('user_id')
name = data.get('name')
cash = data.get('cash')
session_id = data.get('session_id')
tokens = data.get('tokens')
price = data.get('price')


user_id = data_session.get('user_id')
name = data_session.get('name')
cash = data_session.get('cash')
session_id = data_session.get('session_id')
tokens = data_session.get('tokens')
price = data_session.get('price')

# print(data.get("name"))

# confirm = add_data_user(data)
# print(data)

# user_id = 2  # Замените на нужный user_id
# new_cash_value = 100.0  # Замените на нужное значение cash
# result = update_data_user(data)

# user_id = 2
# confirm = get_data_user(user_id)
# print(confirm)

# add_data_session(data_session)
# print(data)

user_id = 4
conf = get_data_session(user_id)
print(conf)