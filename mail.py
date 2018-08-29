#!/usr/bin/python
# coding: UTF-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
def sendMail( text ):
    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="nanjizhiyin@163.com"    #用户名
    mail_pass="wu5211314"   #口令
    sender = 'nanjizhiyin@163.com'
    receivers = ['gaojindan@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = sender   # 发送者
    message['To'] =  ";".join(receivers)        # 接收者

    subject = '可以买了'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")