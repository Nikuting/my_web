# -*- coding: UTF-8 -*- #

from flask import Flask, redirect,render_template, session, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap  #推特做的CSS框架
from flask_moment import Moment        #本地化日期和时间包
from flask_wtf import FlaskForm    #tf扩展的表单类
from wtforms import StringField, SubmitField    #1.文本字段类，2.提交表单类
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy  #导入数据库
from flask_mail import Mail, Message   #导入包装了smtplib的扩展
from threading import Thread #异步不同线程
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
basedir = os.path.abspath(os.path.dirname(__file__))    #得到当前文件根目录的绝对路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db?check_same_thread=False') #创建数据库URL
#data.db后面的？的一段是为了保证session在同一个theard中运行，否则会报错
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True   #每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#配置Flask-Mail来使用Email发送邮件
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '1740454139@qq.com'
app.config['MAIL_PASSWORD'] = 'ndcmpuzxyzofdeii'

#集成发送mail消息功能
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flask of Daxia]'   #定义邮件主题的前缀
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <1740454139@qq.com>'   #定义发件人地址

mail = Mail(app)  #实例化Mail
db = SQLAlchemy(app)  #实例化数据库
bootstrap = Bootstrap(app)
moment = Moment(app)

#电子邮件功能支持
def send_eamil(to, subject, template, **kwargs):
    #用Message类定义发送的主题，发收件人
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=
                  app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_asyn_email, args=[app, msg])
    thr.start()
    return thr

#异步发送电子邮件
def send_asyn_email(app, msg):
    with app.app_context():
        mail.send(msg)



#定义数据库模型（即一个模型代表一个表）
class Role(db.Model):
    __tablename__ = 'roles'  #设置类在数据库中使用的表名，
    id = db.Column(db.Integer, primary_key=True)  #定义Role表主键
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):      #返回一个具有可读性的字符串表示模型，调试或测试中使用
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  #定义role_id为外键，为roles表的id值
    #即这一列代表user对应的role

    def __repr__(self):
        return '<User %r>' % self.username

#定义POST的表单类
class NameForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])  #实例化文本字段
    submit = SubmitField('Submit')      #实例化提交按钮

#主页网页
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():   #验证表单，即DataRequired()函数是否验证成功
        user = User.query.filter_by(username=form.name.data).first()  #如果数据库中有对应的用户则赋给user
        if user is None:        #如果没有哪就以POST的表单用户名在数据库中建立对应值
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False #数据库中是否有该用户，来输出不同的欢迎语
            send_eamil('1014586949@qq.com', 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name=session.get('name'), known=session.get('known', False), current_time = datetime.utcnow())

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