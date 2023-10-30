
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    full_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    red_flags = relationship('Red_flag', back_populates='user')
    interventions = relationship('Intervention', back_populates='user')
    notifications = relationship('Notification', back_populates='user')
    admin_actions = relationship('AdminAction', back_populates='user')



class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    attachments = Column(String)
    additional_details = Column(Text)
    location_lat = Column(Float)
    location_long = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))

    user = relationship("User", back_populates="interventions")
    status = relationship("Status", back_populates="interventions")
    red_flags = relationship("RedFlag", secondary="tags")
    images = relationship("Image", back_populates="intervention")
    videos = relationship("Video", back_populates="intervention")

