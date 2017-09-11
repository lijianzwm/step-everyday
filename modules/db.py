# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, Date, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config
from logger import logger
import traceback

Base = declarative_base()

class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    email = Column(Integer)
    date = Column(Date)
    content = Column(String)

    def get_content(self):
        return self.content

    def get_date(self):
        return self.date

class DB:

    def __enter__(self):
        engine = create_engine('mysql+pymysql://%s:%s@%s:%d/%s' %
                               (Config.MYSQL_USER, Config.MYSQL_PASSWD, Config.MYSQL_HOST, Config.MYSQL_PORT,
                                Config.MYSQL_DB))
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


    def select_content(self, dt_list, email):
        if type(dt_list) != list:
            raise Exception("select_content_by_dt_list: dt must be list")
        query_result = self.session.query(Note).filter(Note.date.in_(dt_list), Note.email == email).all()
        result = ["<div>------" + str(r.get_date()) + "------</div>" + str(r.get_content()) for r in query_result]
        return result

    def add_note(self, email, content, dt):
        note = Note(email=email, date=dt, content=content)
        self.session.add(note)



