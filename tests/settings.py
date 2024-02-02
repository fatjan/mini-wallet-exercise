from app.settings import get_db_uri
from environs import Env

env = Env()
env.read_env()

db_name = env.str("TEST_DB_NAME")
DATABASE_URI = get_db_uri(db_name=db_name)

ENV = "test"
TESTING = True
SQLALCHEMY_DATABASE_URI = DATABASE_URI
BCRYPT_LOG_ROUNDS = 4
DEBUG_TB_ENABLED = False
DEBUG = False
SECRET_KEY = env.str("SECRET_KEY")
SQLALCHEMY_TRACK_MODIFICATIONS = False
