import datetime

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    UnicodeText,
    DateTime,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    tite = Column(UnicodeText(length=128), unique=True)
    text = Column(UnicodeText(length=None))
    created = Column(DateTime, default=datetime.datetime.utcnow)

Index('my_index', Entry.tite, unique=True, mysql_length=255)
