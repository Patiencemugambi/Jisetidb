from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



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

