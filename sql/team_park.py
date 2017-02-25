from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from mlb_database import Base


class ParkEntry(Base):

    __tablename__ = 'park_entries'

    park_year = Column(String, primary_key=True)
    home_team = Column(String, primary_key=True)
    park_hitter_score = Column(Float)
    park_pitcher_score = Column(Float)

    def __init__(self, home_team, park_year):
        self.home_team = home_team
        self.park_year = park_year
