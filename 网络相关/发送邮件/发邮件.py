# coding: utf-8
#!/usr/bin/python
from email.mime.text import MIMEText
import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header


#传入'plain'表示纯文本
msg = MIMEText('邮件正文', 'plain', 'utf-8')



# 输入Email地址和口令:
from_addr = "sdf63fg@yeah.net"
password = "72046437"
# 输入收件人地址:
to_addr ="260848373@qq.com"
# 输入SMTP服务器地址:
smtp_server = "smtp.yeah.net"

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

msg['From'] = _format_addr('发件人名称 <%s>' % from_addr)
msg['To'] = _format_addr('收件人名称 <%s>' % to_addr)
msg['Subject'] = Header('主题', 'utf-8').encode()


# SMTP协议默认端口是25
server = smtplib.SMTP(smtp_server, 25) 
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
