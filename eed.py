import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"
mail_user = "taomi208874@163.com"
mail_pass = "VDNZXWOSIMGOWIVK"
receivers = '840883302@qq.com'
message = MIMEText("Thanks for using our web", 'plain', 'utf-8')
subject = 'Your CAPTCHA: '+'1234'
message['Subject'] = Header(subject, 'utf-8')
try:
    smtpObj = SMTP_SSL(mail_host)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(mail_user, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")


