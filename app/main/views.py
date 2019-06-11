# -*- coding: UTF-8 -*- #

from datetime import datetime
from flask import redirect,render_template, session, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_eamil

@main.route('/', methods=['GET', 'POST'])  #路由修饰器由蓝本提供
def index():
    form = NameForm()
    if form.validate_on_submit():  # 验证表单，即DataRequired()函数是否验证成功
        user = User.query.filter_by(username=form.name.data).first()  # 如果数据库中有对应的用户则赋给user
        if user is None:  # 如果没有哪就以POST的表单用户名在数据库中建立对应值
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False  # 数据库中是否有该用户，来输出不同的欢迎语
            send_eamil('1014586949@qq.com', 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))  #端点前要加蓝本名字
    return render_template("index.html", form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())