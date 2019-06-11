# -*- coding: UTF-8 -*- #

from . import db

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
