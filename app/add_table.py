import psycopg2
from keys import user_db, paswor_db

print(user_db, paswor_db)

# Устанавливаем соединение с базой данных
connection = psycopg2.connect(host="localhost", database="my_database", user=user_db, password=paswor_db)

def create_database():
    try:
        conn = connection.cursor()

        # Создание таблицы users
        conn.execute('''
            CREATE TABLE users_telegram (
                id BIGINT PRIMARY KEY UNIQUE,
                name VARCHAR(50),
                full_name VARCHAR(50),
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                chat_id BIGINT,
                is_admin BOOLEAN DEFAULT FALSE,
                is_block BOOLEAN DEFAULT FALSE,
                is_good INTEGER DEFAULT 3
                        );
            
            CREATE TABLE settings (
                id BIGINT PRIMARY KEY,
                temp_chat FLOAT DEFAULT 0.7,
                frequency FLOAT DEFAULT 0.5,
                presence FLOAT DEFAULT 0.5,
                flag_stik BOOLEAN DEFAULT FALSE,
                all_count INTEGER DEFAULT 0,
                all_token INTEGER DEFAULT 0,
                the_gap FLOAT DEFAULT 0.05,
                set_model VARCHAR(50) DEFAULT 'gpt-4o-mini',
                time_money TIMESTAMP,
                currency VARCHAR(50),
                give_me_money FLOAT DEFAULT 0,
                money FLOAT DEFAULT 30,
                all_in_money FLOAT DEFAULT 0,
                FOREIGN KEY (id) REFERENCES users_telegram(id)
                        );
                     
            CREATE TABLE discussion (
                id BIGINT PRIMARY KEY,
                discus VARCHAR(10000),
                timestamp TIMESTAMP,
                FOREIGN KEY (id) REFERENCES users_telegram(id)
                        );      

            CREATE TABLE exchange (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                rate FLOAT DEFAULT 100
                        );
                     
            CREATE TABLE statistics (
                id SERIAL PRIMARY KEY,
                time TIMESTAMP,
                use_model VARCHAR(50),
                sesion_token INTEGER DEFAULT 0,
                price_1_tok FLOAT DEFAULT 0,
                price_sesion_tok FLOAT DEFAULT 0,
                users_telegram_id BIGINT,
                FOREIGN KEY (users_telegram_id) REFERENCES users_telegram(id)
                        );
            
            CREATE TABLE voice_messages (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,                   -- ID чата
                file_id VARCHAR(255),             -- ID файла
                transcript TEXT,                  -- Расшифровка текста из речи
                gpt_response TEXT,                -- Ответ от GPT
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Время создания
                FOREIGN KEY (chat_id) REFERENCES users_telegram(id)
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

