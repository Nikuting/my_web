# -*- coding: UTF-8 -*- #

from flask import Flask, redirect,render_template, session, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap  #推特做的CSS框架
from flask_moment import Moment        #本地化日期和时间包
from flask_sqlalchemy import SQLAlchemy  #导入数据库
from flask_mail import Mail, Message   #导入包装了smtplib的扩展
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  #导入不同的配置对象
    config[config_name].init_app(app)

    from .main import main as main_blueprint    #将蓝本用函数注册到程序上
    app.register_blueprint(main_blueprint)

    #初始化各个扩展
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    return app