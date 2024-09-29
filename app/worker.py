
import sqlite3
conn = sqlite3.connect('./db/db.litesql')














#### USERS:


# Чтение данных USERS:
def get_data_user(user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT * FROM users WHERE user_id = ?;
            ''',
            (user_id,) 
        )

        user = cursor.fetchone()
        cursor.close()
        return user
    
    except Exception as e:
        return f"Error get data user {e}"



# Добавление USERS:
def add_data_user(data):
    try:
        user_id = data.get("user_id")

        if not user_id:
            return False

        keys, values, drop = [], [], []
    
        for key, value in data.items():
            keys.append(key)
            values.append(value)
            drop.append("?")

        keys = ", ".join(keys)
        drop = ", ".join(drop)

        cursor = conn.cursor()
        cursor.execute(
            f'''
            INSERT INTO users ({keys}) VALUES ({drop}) 
            ''', 
            (*values,) 
        )  # Передаем только values в execute()

        conn.commit()
        cursor.close()
        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        return False 


# data = {
#     #"name": 'Anny',
#     "user_id": 10,
#     #"cash": 15000,
# }

# data = add_data_user(data)
# print(data)

# data_2 = get_data_user(10)
# print(data_2)


# Обновление данных USERS:
def update_data_user(data):
    try:
        user_id = data.get("user_id")

        if not user_id:
            return False

        key_dict, value_dic = [], []

        for key, value in data.items():
            if key != "user_id":
                key_dict.append(f"{key} = ?")
                value_dic.append(value)

        if not key_dict:
            return False

        key_dict = ", ".join(key_dict)
        value_dic.append(user_id)

        cursor = conn.cursor()
        cursor.execute(
            f'''
                UPDATE users SET {key_dict} WHERE user_id = ?
            ''',
                (*value_dic,)
        )

        conn.commit()
        cursor.close()
        return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False




# data = {
#     #"name": 'Jopa',
#     "user_id": 8,
#     #"cash": 3,
# }

# data = update_data_user(data)
# print(data)

# # data_2 = get_data_user(8)
# # print(data_2)