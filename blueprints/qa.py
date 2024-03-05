from flask import Blueprint, request, render_template, g, redirect, url_for
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required
bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=questions)


@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo:跳转到问答详情页
            return redirect(url_for("qa.index"))
        else:
            print(form.errors)
            # 重定向到问答的提交页面
            return redirect(url_for("qa.public_question"))


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


@bp.route("/answer/public", methods=['POST'])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(question_id=question_id, content=content, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.qa_detail', qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('qa.qa_detail', qa_id=request.args.get('qa_id')))


@bp.route("/search")
def search():
    # 获取到用户输入的方式：
    # /search?q=flask查询字符串形式
    # /search/<q>把关键字固定到路径当中
    # post请求，request.form拿到请求
    q = request.args.get('q')
    # 过滤方式：
    # 根据标题过滤
    # 根据内容过滤
    # 根据内容或标题过滤（以上两者的结合）
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html", questions=questions)
