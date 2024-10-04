import os
from dotenv import load_dotenv
load_dotenv()

user = os.environ.get('USER_DB')
password = os.environ.get('PASWOR_DB')
database = os.environ.get('DB_NAME', 'my_database')
host = os.environ.get('DB_HOST', 'localhost')  
    


