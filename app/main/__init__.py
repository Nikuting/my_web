# -*- coding: UTF-8 -*- #

from flask import Blueprint

main = Blueprint('main', __name__)

#为了避免循环导入依赖，因为再view.py和errors.py种还要导入蓝本main
from . import views, errors   #导入这两个模块将路由和错误处理程序与蓝本关联起来
