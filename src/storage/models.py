from sqlalchemy import Column, Integer, String, Date, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    site = Column(String, nullable=False)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    stipend = Column(String)
    location = Column(String)
    link = Column(String, unique=True, nullable=False)
    deadline = Column(String)
    posted_date = Column(String)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_sent = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Job(company='{self.company}', role='{self.role}', site='{self.site}')>"

class SentNotification(Base):
    __tablename__ = 'sent_notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.utcnow().date)
    jobs_sent_count = Column(Integer, default=0)
    channel = Column(String) # email/telegram

    def __repr__(self):
        return f"<SentNotification(date='{self.date}', count={self.jobs_sent_count}, channel='{self.channel}')>"
