from sqlalchemy import Column, Integer, String, Float, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from mlb_database import Base


class GameEntry(Base):

    __tablename__ = 'game_entries'

    game_date = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)
    home_team = Column(String, primary_key=True)
    away_team = Column(String)

    umpire = Column(String)
    wind_speed = Column(Integer)
    temperature = Column(Float)

    pitcher_pregame_entries = relationship('PregamePitcherGameEntry', backref='game_entry')
    pitcher_postgame_entries = relationship('PostgamePitcherGameEntry', backref='game_entry')
    hitter_pregame_entries = relationship('PregameHitterGameEntry', backref='game_entry')
    hitter_postgame_entries = relationship('PostgameHitterGameEntry', backref='game_entry')

    def __init__(self, game_date, game_time, home_team, away_team):
        self.game_date = game_date
        self.game_time = game_time
        self.home_team = home_team
        self.away_team = away_team
