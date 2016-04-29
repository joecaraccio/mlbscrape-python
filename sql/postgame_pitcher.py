from sqlalchemy import Column, Integer, String, Float

from mlb_database import Base


# Baseball player class
class PostgamePitcherGameEntry(Base):
    __tablename__ = 'postgame_pitcher_entries'

    rotowire_id = Column(String, primary_key=True)
    game_date = Column(String, primary_key=True)
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
        self.draftkings_salary = 0

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




