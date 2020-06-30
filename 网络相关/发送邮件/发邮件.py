# -*- coding: UTF-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header


#text：发送邮件的正本内容
def send_mail(text):     
    #传入'plain'表示纯文本
    content = MIMEText(text, 'plain', 'utf-8')

    # 构建并添加图像对象
    file = open(r"C:\Users\hewei\Pictures\a.png",'rb')
    img_data = file.read()
    file.close()
    img = MIMEImage(img_data)
    img.add_header('Content-Disposition', 'attachment', filename="test.png")
    

    msg = MIMEMultipart()
    msg.attach(content)
    msg.attach(img)

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

    msg['From'] = _format_addr('openwrt <%s>' % from_addr)
    msg['To'] = _format_addr('何威 <%s>' % to_addr)
    msg['Subject'] = Header('邮件正文', 'utf-8').encode()



    # SMTP协议默认端口是25
    server = smtplib.SMTP(smtp_server, 25) 
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


send_mail("test")
