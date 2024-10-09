import psycopg2
from keys import user, password

print(user, password)

connection = psycopg2.connect(host="localhost", database="my_database", user=user, password=password)

def create_database():
    try:
        conn = connection.cursor()

        # Создание таблицы users
        conn.execute('''
            CREATE TABLE users (
                user_id BIGINT PRIMARY KEY,
                name VARCHAR(50),
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                set_model VARCHAR(50),
                all_count INTEGER DEFAULT 0,
                all_token INTEGER DEFAULT 0,
                is_admin BOOLEAN DEFAULT FALSE,
                date TIMESTAMP
            );
        ''')

# all_count — общее количество запросов, выполненных пользователем.
# all_token — общее количество токенов, использованных пользователем.
# set_model — текущая модель GPT, установленная пользователем.
# money — текущий баланс пользователя в рублях.
# timestamp — дата и время создания записи.

        # Создание таблицы statistics
        conn.execute('''
            CREATE TABLE session (
                user_id BIGINT PRIMARY KEY,
                use_model VARCHAR(50),
                sesion_token INTEGER DEFAULT 0, 
                price_1_tok FLOAT,
                price_session_tok FLOAT,
                money FLOAT DEFAULT 50,
                date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        ''')


        # Сохраняем изменения
        connection.commit()

        print("Таблицы успешно созданы.")
    
    except Exception as e:
        print(f"Ошибка: {e}")
    
    finally:
        # Закрываем соединение
        conn.close()
        connection.close()

# Вызов функции для создания базы данных
create_database()


