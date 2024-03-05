import string

from flask import Blueprint, render_template, redirect, request, jsonify, url_for, flash, abort, session
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from exts import mail, db, r, cache
import random
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在")
                return redirect("auth.login")
            if check_password_hash(user.password, password):
                # cookie
                # cookie中不适合存储太多的数据，只适合存储少量数据
                # cookie一般用来存放登录授权的东西
                # flask中的session是经过加密后存储在cookie中的
                session["user_id"] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))
    # 验证用户提交的邮箱和验证码是否对应正确
    # 表单验证：flask-wtf:wtforms


@bp.route('/mail/test')
def mail_test():
    message = Message('test', recipients=['2769715225@qq.com'], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"


@bp.route('/captcha/email')
def get_captcha_email():
    email = request.args.get('email')
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = ''.join(captcha)
    message = Message('知了传课验证码', recipients=['2769715225@qq.com'], body=f"你的验证码是{captcha}")
    mail.send(message)
    # 用数据库方式存储验证码
    # email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    # db.session.add(email_captcha)
    # db.session.commit()
    # 用redis键值对方式存储
    # r.set(email, captcha)
    # 用缓存的方式存储
    cache.set(email, captcha)
    return jsonify({'code': 200, 'message': '', 'data': None})


@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")
