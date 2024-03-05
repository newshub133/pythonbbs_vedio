from flask import Flask, session, g
import config
from exts import db, mail
from models import UserModel
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from flask_migrate import Migrate
from exts import cache
app = Flask(__name__)
app.config.from_object(config)


db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)
cache.init_app(app)

# hook
# 钩子函数：before_request/before_first_request/after_request
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        # 将用户信息绑定到全局变量上
        setattr(g, 'user', user)
    else:
        setattr(g, "user", None)


# 上下文处理函数，返回的变量在模板(templates)文件中可以直接使用
@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
