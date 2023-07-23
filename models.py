from sqlalchemy import Column, Integer, Float, ForeignKey, String, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import numpy as np
import typing

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
    image_id = Column(Integer, ForeignKey("imgs.id"))
    occluded = Column(Float)
    occlusions = Column(Integer)

    def __init__(self, xcenter: int, ycenter: int, a: float, b: float, rotation: float, angle_range: typing.List[typing.Tuple[float, float]]):
        self.x = xcenter
        self.y = ycenter
        self.a = a
        self.b = b
        self.theta = rotation
        self.angle_range = angle_range
        self.occlusions = len(angle_range)
        self.occluded = 1 - (np.sum([i[1] - i[0] for i in angle_range]) / np.pi / 2)
        self.image = None


class Img(Base):
    __tablename__ = 'imgs'
    id = Column(Integer, primary_key=True)
    img_filepath = Column(String)
    particles = relationship('EllipticalParticle', back_populates='image')

