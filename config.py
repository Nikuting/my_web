# -*- coding: UTF-8 -*- #

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '123456'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 集成发送mail消息功能
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flask of Daxia]'  # 定义邮件主题的前缀
    FLASKY_MAIL_SENDER = 'Flasky Admin <1740454139@qq.com>'  # 定义发件人地址

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '1740454139@qq.com'
    MAIL_PASSWORD = 'ndcmpuzxyzofdeii'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db?check_same_thread=False')

class TestConfig(Config):
    TESTTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.db?check_same_thread=False')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db?check_same_thread=False')

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}