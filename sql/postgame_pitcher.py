from sqlalchemy import Column, Integer, String, Float, Boolean
from mlb_database import Base
from sqlalchemy import ForeignKey, ForeignKeyConstraint


class PostgamePitcherGameEntry(Base):
    """ Class for storing a SQL entry of the  actual stats for a pitcher
    Many-to-one relationship with PitcherEntry
    """
    __tablename__ = 'postgame_pitcher_entries'

    rotowire_id = Column(String, ForeignKey('pitcher_entries.rotowire_id'), primary_key=True)
    game_date = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)
    home_team = Column(String)
    is_home_team = Column(Boolean)
    __table_args__ = (ForeignKeyConstraint([game_date, game_time, home_team],
                                           ['game_entries.game_date', 'game_entries.game_time', 'game_entries.home_team']), {})

    actual_draftkings_points = Column(Float)

    # Game stats
    game_ip = Column(Float)
    game_so = Column(Integer)
    game_wins = Column(Integer)
    game_er = Column(Integer)
    game_h = Column(Integer)
    game_bb = Column(Integer)
    game_hbp = Column(Integer)
    game_cg = Column(Integer)
    game_cgso = Column(Integer)
    game_no_hitter = Column(Integer)

    def __init__(self):
        """ Constructor
        Copy the Pitcher object into the PitcherGameEntry fields
        :param pitcher: Pitcher object
        """

        self.actual_draftkings_points = 0

        # Season stats
        self.game_ip = 0
        self.game_so = 0
        self.game_wins = 0
        self.game_er = 0
        self.game_h = 0
        self.game_bb = 0
        self.game_hbp = 0
        self.game_cg = 0
        self.game_cgso = 0
        self.game_no_hitter = 0

    def __repr__(self):
        """
        :return: string representation identifying the Pitcher entry
        """
        return "<Pitcher game entry(name='%s')>" % self.rotowire_id




