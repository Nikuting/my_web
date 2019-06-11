# -*- coding: UTF-8 -*- #

from flask import render_template
from .__init__ import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)  #注册程序全局的错误处理程序，故而使用app_errorhandler()
def internal_server_error(e):
    return render_template('500.html'), 500