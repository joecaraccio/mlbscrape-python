from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from mlb_database import Base


class GameEntry(Base):

    __tablename__ = 'game_entries'

    game_date = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)
    home_team = Column(String)
    away_team = Column(String)

    ump_ks_per_game = Column(Float)
    ump_runs_per_game = Column(Float)
    park_hitter_score = Column(Float)
    park_pitcher_score = Column(Float)
    wind_speed = Column(Integer)

    pitcher_pregame_entries = relationship('PregamePitcherGameEntry', backref='game_entry')
    pitcher_postgame_entries = relationship('PostgamePitcherGameEntry', backref='game_entry')

    def __init__(self, game_date, game_time, home_team, away_team):
        self.game_date = game_date
        self.game_time = game_time
        self.home_team = home_team
        self.away_team = away_team
