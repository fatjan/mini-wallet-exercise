def get_db_uri(db_name):
    return f"mysql+pymysql://root@localhost:3306/{db_name}"

DATABASE_URI = get_db_uri(db_name="wallet_db")
ENV = "dev"
DEBUG = True
SQLALCHEMY_DATABASE_URI = DATABASE_URI
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "secret_key"