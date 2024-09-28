
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

    # Инициализируем списки для ключей и значений
    key_dict, value_dict = [],[]

    # Формирование списков ключей и значений
    for key, value in data.items():
        if key != "user_id": 
            key_dict.append(key)
            value_dict.append(value)

    # Преобразуем список ключей в строку, разделенную запятыми
    key_dict = ", ".join(key_dict)

    # Подготавливаем строки для плейсхолдеров значений
    value_dict = ", ".join(['?'] * len(value_dict))
# 
    try:
        cursor = conn.cursor()
        cursor.execute(
            f'''
            INSERT INTO users ({key_dict}) 
            VALUES ({value_dict})
            ''', value_dict
        )

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
  
    value_dict = ", ".join(['?'] * len(value_dict))
    print(key_dict)
    # print()
    print(value_dic)

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