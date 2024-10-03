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
                created_at TIMESTAMP,
                last_active TIMESTAMP,
                date TIMESTAMP
            );
        ''')

        # Создание таблицы session
        conn.execute('''
            CREATE TABLE session (
                session_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                tokens FLOAT,
                price FLOAT,
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
