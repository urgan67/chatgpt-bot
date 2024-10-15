import os
from dotenv import load_dotenv
load_dotenv()

user_db = os.environ.get('USER_DB')
paswor_db = os.environ.get('PASWOR_DB')
database = os.environ.get('DB_NAME', 'my_database')
host = os.environ.get('DB_HOST', 'localhost')  
token = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY')
api_key = os.environ.get('CHATGPT_API_KEY')
white_list = os.environ.get('WHITE_LIST')
admin_user_ids = os.environ.get('ADMIN_USER_IDS')
block = os.environ.get('ALLOWED_TELEGRAM_USER_IDS')