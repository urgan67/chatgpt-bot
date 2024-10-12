import psycopg2
from keys import user, password

print(user, password)

# Устанавливаем соединение с базой данных
connection = psycopg2.connect(host="localhost", database="my_database", user=user, password=password)

def create_database():
    try:
        conn = connection.cursor()

        # Создание таблицы users
        conn.execute('''
            CREATE TABLE users (
                user_id BIGINT PRIMARY KEY NOT NULL,
                name VARCHAR(100),
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100),
                full_name VARCHAR(100),
                all_count INTEGER NOT NULL DEFAULT 0,
                all_token INTEGER NOT NULL DEFAULT 0,
                set_model VARCHAR(50) NOT NULL DEFAULT 'gpt-3.5-turbo-0613',
                currency VARCHAR(50),
                give_me_money FLOAT NOT NULL DEFAULT 0,
                money FLOAT NOT NULL DEFAULT 100,
                all_in_money FLOAT NOT NULL DEFAULT 0,
                time_money TIMESTAMP,
                discus VARCHAR(10000),
                created_at TIMESTAMP
            );
        ''')

        # User spending statistics - One-to-many
        conn.execute('''
            CREATE TABLE statistics (
                id SERIAL PRIMARY KEY,
                time TIMESTAMP,
                use_model VARCHAR(50) NOT NULL,
                session_token INTEGER NOT NULL DEFAULT 0,
                price_1_tok FLOAT NOT NULL DEFAULT 0,
                price_session_tok FLOAT NOT NULL DEFAULT 0,
                users_telegram_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE
            );
        ''')

        # Сохраняем изменения
        connection.commit()

        print("Таблицы успешно созданы.")
    
    except Exception as e:
        print(f"Ошибка: {e}")
    
    finally:
        # Закрываем соединение
        if conn:
            conn.close()
        if connection:
            connection.close()

# Вызов функции для создания базы данных
create_database()
