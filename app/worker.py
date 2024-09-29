
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
            if key != "user_id":  # Исключаем user_id из списка значений
                keys.append(key)
            values.append(value)
            drop.append("?")

        keys = ", ".join(keys)
        drop = ", ".join(drop)

        cursor = conn.cursor()
        cursor.execute(
            f'''
            INSERT INTO users ({keys}, user_id) VALUES ({drop}, ?) 
            ''', 
            values 
        )  # Передаем только values в execute()
        conn.commit()
        cursor.close()
        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        return False 






# Обновление данных USERS:
def update_data_user(data):

    user_id = data.get("user_id")

    if not user_id:
        return False 

    key_dict, value_dic = [], []

    for key, value in data.items():
        if key != "user_id":
            key_dict.append(f"{key} = ?")
        value_dic.append(value)

    
    key_dict = ", ".join(key_dict)
  
    # value_dict = ", ".join(['?'] * len(value_dict))
    # print(key_dict)
    # # print()
    # print(value_dic)

    try:
        cursor = conn.cursor()
        value_dic.append(user_id)
        cursor.execute(
            f'''
                UPDATE users SET {key_dict} WHERE user_id = ?
            ''',
                (value_dic)
        )
        
        conn.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        cursor.close()