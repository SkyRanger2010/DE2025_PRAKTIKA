from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.database import Base


class UserIn(Base):
    __tablename__ = 'userin'

    userid = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    biography = Column(Text, nullable=True)
    sex = Column(String, nullable=True)
    is_private = Column(Boolean, nullable=True)
    external_url = Column(String, nullable=True)
    account_type = Column(String, nullable=True)
    avatar = Column(Integer, nullable=True)
    is_verified = Column(Boolean, nullable=True)
    follower_count = Column(Integer, nullable=True)
    following_count = Column(Integer, nullable=True)
    media_count = Column(Integer, nullable=True)
    last_time = Column(DateTime, nullable=True)
