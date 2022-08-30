# -*- coding: UTF-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header




#text：发送邮件的正本内容
def send_mail(text):     
    #传入'plain'表示纯文本
    content = MIMEText(text, 'plain', 'utf-8')

    # 构建并添加图像对象
    file = open(r"test.jpg",'rb')
    img_data = file.read()
    file.close()
    img = MIMEImage(img_data)
    img.add_header('Content-Disposition', 'attachment', filename="test.png")

    # 构建并添加其它附件
    file2 = MIMEApplication(open('test.pdf', 'rb').read())
    file2.add_header('Content-Disposition', 'attachment', filename="test.pdf")


    msg = MIMEMultipart()
    msg.attach(content)
    msg.attach(img)
    msg.attach(file2)

    # 输入Email地址和口令:
    from_addr = "sdf63fg@yeah.net"
    password = "12345"
    # 输入收件人地址:
    to_addr ="sdf63fg@yeah.net"
    # 输入SMTP服务器地址:
    smtp_server = "smtp.yeah.net"

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    msg['From'] = _format_addr('openwrt <%s>' % from_addr)
    msg['To'] = _format_addr('何威 <%s>' % to_addr)
    msg['Subject'] = Header('邮件正文', 'utf-8').encode()



    # SMTP协议默认端口是25
    server = smtplib.SMTP(smtp_server, 25) 
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


#发送任意格式的附件
def send_file(text):
    database=open('test.jpg','rb').read()
    #传入'plain'表示纯文本
    content = MIMEText(text, 'plain', 'utf-8')

    msg = MIMEMultipart()
    msg.attach(content)
    
    if database !=None:
            # 构建并添加db
        db = MIMEApplication(database)
        db.add_header('Content-Disposition', 'attachment', filename='test.jpg')   
        msg.attach(db)

    # 输入Email地址和口令:
    from_addr = "sdf63fg@yeah.net"
    password = "123456"
    # 输入收件人地址:
    to_addr ="sdf63fg@yeah.net"
    # 输入SMTP服务器地址:
    smtp_server = "smtp.yeah.net"


    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    msg['From'] = _format_addr('驻在员 <%s>' % from_addr)
    msg['To'] = _format_addr('何威 <%s>' % to_addr)
    msg['Subject'] = Header('客户不良信息数据库', 'utf-8').encode()

    # SMTP协议默认端口是25
    server = smtplib.SMTP(smtp_server, 25) 
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())


#send_mail("test")
send_file("test")
