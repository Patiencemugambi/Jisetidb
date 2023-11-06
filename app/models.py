from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

    red_flags = relationship("RedFlag", back_populates="user")
    interventions = relationship("Intervention", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    admin_actions = relationship("AdminAction", back_populates="user")

class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    record_type = Column(String)

    red_flags = relationship("RedFlag", back_populates="status")
    interventions = relationship("Intervention", back_populates="status")

class RedFlag(Base):
    __tablename__ = "red_flags"

    id = Column(Integer, primary_key=True, index=True)
    incident_type = Column(String)
    description = Column(Text)
    attachments = Column(String)
    additional_details = Column(Text)
    county = Column(String, nullable=True)
    location = Column(String)
    date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="red_flags")
    status = relationship("Status", back_populates="red_flags")
    images = relationship("Image", back_populates="red_flag")
    videos = relationship("Video", back_populates="red_flag")

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    attachments = Column(String)
    additional_details = Column(Text)
    county = Column(String)
    location = Column(String)

    user = relationship("User", back_populates="interventions")
    status = relationship("Status", back_populates="interventions")
    images = relationship("Image", back_populates="intervention")
    videos = relationship("Video", back_populates="intervention")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    red_flag_id = Column(Integer, ForeignKey("red_flags.id"))
    intervention_id = Column(Integer, ForeignKey("interventions.id"))

    red_flag = relationship("RedFlag", backref="tags")
    intervention = relationship("Intervention", backref="tags")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    red_flag_id = Column(Integer, ForeignKey("red_flags.id"))
    intervention_id = Column(Integer, ForeignKey("interventions.id"))
    file_path = Column(String)

    red_flag = relationship("RedFlag", back_populates="images")
    intervention = relationship("Intervention", back_populates="images")

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    red_flag_id = Column(Integer, ForeignKey("red_flags.id"))
    intervention_id = Column(Integer, ForeignKey("interventions.id"))
    file_path = Column(String)

    red_flag = relationship("RedFlag", back_populates="videos")
    intervention = relationship("Intervention", back_populates="videos")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    is_email = Column(Boolean)
    is_sms = Column(Boolean)

    user = relationship("User", back_populates="notifications")

class AdminAction(Base):
    __tablename__ = "admin_actions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    record_id = Column(Integer)
    action = Column(String)
    timestamp = Column(String)

    user = relationship("User", back_populates="admin_actions")
