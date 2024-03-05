from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import redis
from flask_caching import Cache

db = SQLAlchemy()
mail = Mail()
r = redis.StrictRedis(host='localhost', port=6379, db=0)
cache = Cache()
