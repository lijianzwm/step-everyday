# -*- coding:utf-8 -*-
"""定时提醒模块"""
import datetime
from modules.db import DB
from modules.mail import MailBox
from config import Config
from modules.mail import MailSender

class Reminder:

    interval = [1, 2, 7, 14, 30, 90]  # 时间间隔，单位是天

    def __init__(self):
        pass

    def _review_date(self):
        dt = []
        today = datetime.date.today()
        for d in self.interval:
            dt.append((today-datetime.timedelta(days=d)).strftime('%Y-%m-%d'))
        return dt


    def _generate_review_note(self):
        """整成复习笔记，返回dict"""
        dt_list = self._review_date()
        user_email = Config.RECEIVE_LIST
        review_note = {}
        for email in user_email:
            with DB() as db:
                merged_content = "\n\n\n".join(db.select_content(dt_list=dt_list, email=email))
                review_note[email] = merged_content

        return review_note


    def remind(self):
        email2note = self._generate_review_note()
        title = datetime.date.today().strftime('%Y-%m-%d')+"复习内容"
        with MailSender() as box:
            for addr, note in email2note.items():
                box.send(addr, title, note)


    def fetch(self):
        with MailBox() as mb:
            mail_list = mb.receive()
            mb.save(mail_list)
            mb.delete()




