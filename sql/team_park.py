from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from mlb_database import Base
import numpy as np


class ParkEntry(Base):

    __tablename__ = 'park_entries'

    home_team = Column(String, primary_key=True)
    park_year = Column(String, primary_key=True)
    park_hitter_score = Column(Float)
    park_pitcher_score = Column(Float)

    def __init__(self, home_team, park_year):
        self.home_team = home_team
        self.park_year = park_year

    def to_input_vector(self):
        return np.array([self.park_hitter_score, self.park_pitcher_score])