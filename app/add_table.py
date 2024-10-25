import psycopg2
from keys import user_db, paswor_db



# Устанавливаем соединение с базой данных
connection = psycopg2.connect(host="localhost", database="my_database", user=user_db, password=paswor_db)

def create_database():
    try:
        conn = connection.cursor()

        # Создание таблицы users
        conn.execute('''
            CREATE TABLE users (
                user_id BIGINT,
                name VARCHAR(100),
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                full_name VARCHAR(100),
                all_count INTEGER,
                all_token INTEGER,
                set_model VARCHAR(50) DEFAULT 'gpt-3.5-turbo',
                currency VARCHAR(50),
                give_me_money FLOAT,
                money FLOAT,
                all_in_money FLOAT,
                time_money TIMESTAMP,
                discus VARCHAR(10000),
                use_model VARCHAR(50),
                session_token INTEGER,
                price_1_tok FLOAT,
                price_session_tok FLOAT,
                tts_1_enabled BOOLEAN DEFAULT FALSE,
                tts_1_hd_enabled BOOLEAN DEFAULT FALSE,
                time TIMESTAMP,
                created_at TIMESTAMP
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




 