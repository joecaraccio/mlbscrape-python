
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class PostgameHitterGameEntry(Base):
    """ Class for SQL entry for a single game played by a hitter
    """
    __tablename__ = 'postgame_hitter_entries'

    rotowire_id = Column(String, ForeignKey("hitter_entries.rotowire_id"), primary_key=True)
    game_date = Column(String, primary_key=True)
    actual_draftkings_points = Column(Float)

    # Game stats
    game_h = Column(Integer)
    game_bb = Column(Integer)
    game_hbp = Column(Integer)
    game_r = Column(Integer)
    game_sb = Column(Integer)
    game_hr = Column(Integer)
    game_rbi = Column(Integer)
    game_1b = Column(Integer)
    game_2b = Column(Integer)
    game_3b = Column(Integer)

    def __init__(self):
        """ Constructor
        :param hitter: Hitter object to copy the fields from
        """

        self.actual_draftkings_points = 0

        # Game stats
        self.game_h = 0
        self.game_bb = 0
        self.game_hbp = 0
        self.game_r = 0
        self.game_sb = 0
        self.game_hr = 0
        self.game_rbi = 0
        self.game_1b = 0
        self.game_2b = 0
        self.game_3b = 0

    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<Hitter PostGame Entry(id='%s')>" % self.rotowire_id





