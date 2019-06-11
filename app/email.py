# -*- coding: UTF-8 -*- #

from flask_mail import Message   #导入包装了smtplib的扩展
from threading import Thread #异步不同线程
from flask import current_app, render_template
from . import mail

#电子邮件功能支持
def send_eamil(to, subject, template, **kwargs):
    app = current_app._get_current_object()
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
