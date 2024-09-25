from worker import get_data_user,update_data_user,add_session,add_data_user


data = {
    "user_id": 2,
    "name": 'Antony',
    "cash": 1500,
    "session_id": 1,
    "tokens": 100,
    "price": 2,  
}

# print(data.get("name"))

# confirm = add_data_user(data)


user_id = 2
answer = update_data_user(user_id)
print(answer)

# user_id = 21258
# answer = get_data_user(user_id)
# print(answer)


# user_id = 21258
# answer = add_session(user_id)
# print(answer)