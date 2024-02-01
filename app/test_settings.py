from .settings import get_db_uri

DATABASE_URI = get_db_uri(db_name="testdb")
ENV = "test"
TESTING = True
SQLALCHEMY_DATABASE_URI = DATABASE_URI
BCRYPT_LOG_ROUNDS = 4
DEBUG_TB_ENABLED = False
DEBUG = False
SECRET_KEY = "secret_key"