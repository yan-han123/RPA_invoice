import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import zipfile
import os

def send_mail_with_appendix(host, sender, password, receivers):
    # 创建多形式组合邮件
    msg = MIMEMultipart()
    msg['From'] = sender  #发件人邮箱
    msg['To'] = ', '.join(receivers)  #收件人邮箱
    msg['Subject'] = "发票处理结果"  #邮件主题
    msg.attach(MIMEText('b发票处理结果', 'plain'))#邮件正文


    #添加附件excel
    att_excel = MIMEApplication(open('testb.xlsx', 'rb').read(), _subtype='xlsx')
    att_excel["Content-Type"] = 'application/octet-stream'
    att_excel["Content-Disposition"] = 'attachment; filename="testb.xlsx"'
    msg.attach(att_excel)

    # 发送邮件
    try:
        # 创建并登录SMTP服务器
        server = smtplib.SMTP()
        server.connect('smtp.qq.com')
        server.login(sender, password)
        # 发送邮件
        text = msg.as_string()
        server.sendmail(sender, receivers, msg.as_string())
        # 断开STMP服务器链接
        server.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print('Error: 邮件发送失败', e)


#设置服务器信息
def send_mail():
    ## TODO:都改成你自己的。
    host = 'smtp.qq.com'  # 发件人邮箱的SMTP服务器
    sender = '1398476709@qq.com'  # 发件人邮箱账号
    password = 'hjbonxbqryblffhe'  # 发件人邮箱密码（不是qq密码，通过设置--》账户--》开启--》授权码）
    receivers = ['3436683535@qq.com']  # 接收人邮箱账号（可以多个，逗号隔开）

    send_mail_with_appendix(host, sender, password, receivers)
