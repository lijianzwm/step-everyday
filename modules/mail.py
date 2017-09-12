# -*- coding:utf-8 -*-
"""邮件读取/发送模块，utf-8编码，POP协议"""
import poplib
from config import Config
from email import parser
import email
from db import DB
import datetime
import smtplib
from email.mime.text import MIMEText
import traceback
from logger import logger


class Email:

    def __init__(self, from_addr=None, to_addr=None, title=None, content=None):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.title = title
        self.content = content

    def parse_from_msg(self, msg):
        if msg is not None:
            self.from_addr = email.utils.parseaddr(msg.get('from'))[1]
            self.to_addr = email.utils.parseaddr(msg.get('to'))[1]
            subject = msg.get('subject')
            h = email.Header.Header(subject)
            dh = list(email.Header.decode_header(h))
            dh[0] = list(dh[0])
            if dh[0][1] is None:
                dh[0][1] = "utf-8"
            self.title = unicode(dh[0][0], dh[0][1]).encode('utf8')
            self.content = ""
            for part in msg.walk():
                contentType = part.get_content_type()
                if contentType == 'text/plain' or contentType == 'text/html':
                    data = part.get_payload(decode=True)
                    self.content = str(data).decode(part.get_content_charset()).encode("utf-8")

    def __str__(self):
        return '''
            "from": {from_addr},
            "to": {to_addr},
            "title": {title},
            "content": {content}
        '''.format(from_addr=self.from_addr, to_addr=self.to_addr, title=self.title, content=self.content)


class MailBox:

    def __init__(self):
        self.dt = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    def __enter__(self):
        self.conn = poplib.POP3_SSL(Config.MAIL_HOST)
        self.conn.user(Config.MAIL_USER)
        self.conn.pass_(Config.MAIL_PASSWD)
        self.mail_num = self.conn.stat()[0]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.quit()

    def receive(self):
        """只接收指定用户的信件"""
        messages = [self.conn.retr(i) for i in range(1, len(self.conn.list()[1]) + 1)]
        messages = ["\n".join(mssg[1]) for mssg in messages]
        mail_list = [parser.Parser().parsestr(mssg) for mssg in messages]
        email_list = []
        for mail in mail_list:
            email = Email()
            email.parse_from_msg(mail)
            if email.from_addr.strip() in Config.RECEIVE_LIST:
                email_list.append(email)
        return email_list

    def save(self, email_list):
        """将邮件保存到数据库中"""
        with DB() as db:
            for email in email_list:
                db.add_note(email.from_addr, email.content, self.dt)
            db.session.commit()


    def delete(self):
        """删除本次全部信件"""
        for i in range(self.mail_num):
                self.conn.dele(i+1)


class MailSender(object):

    def __enter__(self):
        self.server = smtplib.SMTP()
        self.server.connect(Config.SMTP_HOST)
        self.server.login(Config.MAIL_USER, Config.MAIL_PASSWD)
        self.username = Config.MAIL_USER
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()


    def send(self, addr, title, content):
        """发送邮件，地址，标题，内容"""
        if content != "":
            msg = MIMEText(content, _subtype='html', _charset='utf8')
            msg['Subject'] = title
            msg['From'] = self.username+"@163.com"
            msg['To'] = addr
            try:
                self.server.sendmail(self.username+"@163.com", addr, msg.as_string())
                return True
            except:
                logger.error(traceback.format_exc())
                return False

