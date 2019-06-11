# -*- coding: UTF-8 -*- #

from flask_wtf import FlaskForm    #tf扩展的表单类
from wtforms import StringField, SubmitField    #1.文本字段类，2.提交表单类
from wtforms.validators import DataRequired

#定义POST的表单类
class NameForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])  #实例化文本字段
    submit = SubmitField('Submit')      #实例化提交按钮
