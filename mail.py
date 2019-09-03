"""
Author  : Alan
Date    : 2019/8/29 11:26
Email   : vagaab@foxmail.com
"""

from config import FROM_ADDRESS, TO_ADDRESS, PASSWORD, SMTP, PORT

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr


class Mail:

    def __init__(self):
        self.from_addr = FROM_ADDRESS
        self.password = PASSWORD
        self.to_addr = TO_ADDRESS
        self.server = smtplib.SMTP_SSL(SMTP, PORT)

        self.server.set_debuglevel(1)
        self.server.login(self.from_addr, self.password)

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self, content):
        content = f'<html><hody><p>{content}</p></body></html>'.replace('\n', '<br>')
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = self._format_addr('Python auto-email<%s>' % self.from_addr)
        msg['To'] = self._format_addr('Python <%s>' % self.to_addr)  # to_addr 为str 多个邮箱用，隔开
        msg['Subject'] = Header('来自Python的测试邮件', 'utf-8').encode()

        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())

    def quit(self):
        self.server.quit()
