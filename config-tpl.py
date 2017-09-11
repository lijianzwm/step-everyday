# -*- coding:utf-8 -*-
"""请填写详细信息后，将config-tpl.py重命名为config.py"""

class Config:

    # Mail Config
    MAIL_HOST = "pop.163.com"
    SMTP_HOST = "smtp.163.com"
    MAIL_USER = ""
    MAIL_PASSWD = ""

    # Mysql Config
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "lijian"
    MYSQL_PASSWD = ""
    MYSQL_DB = ""

    # 收件箱白名单，只为这些邮件地址服务
    RECEIVE_LIST = [
        "",
        "",
    ]
