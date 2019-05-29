# -*- coding: UTF-8 -*- #

from flask import Flask, redirect,render_template, session, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap  #推特做的CSS框架
from flask_moment import Moment        #本地化日期和时间包
from flask_wtf import FlaskForm    #tf扩展的表单类
from wtforms import StringField, SubmitField    #1.文本字段类，2.提交表单类
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])  #实例化文本字段
    submit = SubmitField('Submit')      #实例化提交按钮

#主页网页
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():   #验证表单，即DataRequired()函数是否验证成功
        session['name'] = form.name.data
        return redirect(url_for('index'))  #重定向到index路由，即重新运行了一遍index(),此时为GET请求，不运行if语句
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
    #使用get()方法，如果session中没有'name'键值对时，返回默认值None

#404界面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#500界面
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
