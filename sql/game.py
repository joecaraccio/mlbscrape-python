from sqlalchemy import Column, Integer, String, Float
from mlb_database import Base


class GameEntry(Base):

    __tablename__ = 'game_entries'

    game_date = Column(String, primary_key=True)
    home_team = Column(String, primary_key=True)
    away_team = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)

    ump_ks_per_game = Column(Float)
    ump_runs_per_game = Column(Float)
    park_score = Column(Integer)
    wind_speed = Column(Integer)

    #game_hitter_entries = relationship("PregameHitterGameEntry", backref="game_hitter_entries")
    #game_pitcher_entries = relationship("PregamePitcherGameEntry", backref="game_entries")

    def __init__(self, game_date, game_time, home_team, away_team):
        self.game_date = game_date
        self.game_time = game_time
        self.home_team = home_team
        self.away_team = away_team
