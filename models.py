from sqlalchemy import Column, Integer, Float, String, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EllipticalParticle(Base):
    __tablename__ = "particles"
    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    a = Column(Float)
    b = Column(Float)
    theta = Column(Float)
    image = relationship('Img', back_populates='particles')
    occluded = Column(Float)
    occlusions = Column(Integer)


class Img(Base):
    __tablename__ = 'imgs'
    id = Column(Integer, primary_key=True)
    bmp = Column(LargeBinary)
    particles = relationship('EllipticalParticle', back_populates='image')
    movenumber = Column(Integer)
    move = Column(String)
