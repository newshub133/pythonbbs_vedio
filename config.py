
SECRET_KEY = 'secret_key'

# 数据库配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zhiliaooa_course'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2769715225@qq.com"
MAIL_PASSWORD = "ncbupbisybgudfji"
MAIL_DEFAULT_SENDER = "2769715225@qq.com"

# 缓存配置
CACHE_TYPE = "RedisCache"
CACHE_REDIS_HOST = "127.0.0.1"
CACHE_REDIS_PORT = 6379