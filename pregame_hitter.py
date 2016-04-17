
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float
from datetime import date


class PregameHitterGameEntry(Base):
    """ Class for SQL entry for a single game played by a hitter
    """
    __tablename__ = 'pregame_hitter_entries'

    rotowire_id = Column(String, primary_key=True)
    game_id = Column(String, primary_key=True)
    team = Column(String)
    #batting_order = Column(Integer)

    # Season stats
    season_ab = Column(Integer)
    season_h = Column(Integer)
    season_bb = Column(Integer)
    season_so = Column(Integer)
    season_r = Column(Integer)
    season_sb = Column(Integer)
    season_cs = Column(Integer)
    season_hr = Column(Integer)
    season_rbi = Column(Integer)

    # Career stats
    career_ab = Column(Integer)
    career_h = Column(Integer)
    career_bb = Column(Integer)
    career_so = Column(Integer)
    career_r = Column(Integer)
    career_sb = Column(Integer)
    career_cs = Column(Integer)
    career_hr = Column(Integer)
    career_rbi = Column(Integer)

    # Versus stats
    """vs_ab = Column(Integer)
    vs_h = Column(Integer)
    vs_bb = Column(Integer)
    vs_so = Column(Integer)
    vs_hr = Column(Integer)
    vs_rbi = Column(Integer)
    """
    vs_hand_ab = Column(Integer)
    vs_hand_h = Column(Integer)
    vs_hand_bb = Column(Integer)
    vs_hand_so = Column(Integer)
    vs_hand_r = Column(Integer)
    vs_hand_sb = Column(Integer)
    vs_hand_cs = Column(Integer)
    vs_hand_hr = Column(Integer)
    vs_hand_rbi = Column(Integer)

    # Month stats
    recent_ab = Column(Integer)
    recent_h = Column(Integer)
    recent_bb = Column(Integer)
    recent_so = Column(Integer)
    recent_r = Column(Integer)
    recent_sb = Column(Integer)
    recent_cs = Column(Integer)
    recent_hr = Column(Integer)
    recent_rbi = Column(Integer)

    def __init__(self):
        """ Constructor
        :param hitter: Hitter object to copy the fields from
        """

        # Season stats
        self.season_ab = 0
        self.season_h = 0
        self.season_bb = 0
        self.season_so = 0
        self.season_r = 0
        self.season_sb = 0
        self.season_cs = 0
        self.season_hr = 0
        self.season_rbi = 0

        # Career stats
        self.career_ab = 0
        self.career_h = 0
        self.career_bb = 0
        self.career_so = 0
        self.career_r = 0
        self.career_sb = 0
        self.career_cs = 0
        self.career_hr = 0
        self.career_rbi = 0

        # Versus stats
        """
        self.vs_ab = hitter.vs_ab
        self.vs_h = hitter.vs_h
        self.vs_bb = hitter.vs_bb
        self.vs_so = hitter.vs_so
        self.vs_hr = hitter.vs_hr
        self.vs_rbi = hitter.vs_rbi
        """

        self.vs_hand_ab = 0
        self.vs_hand_h = 0
        self.vs_hand_bb = 0
        self.vs_hand_so = 0
        self.vs_hand_r = 0
        self.vs_hand_sb = 0
        self.vs_hand_cs = 0
        self.vs_hand_hr = 0
        self.vs_hand_rbi = 0

        # Month stats
        self.recent_ab = 0
        self.recent_h = 0
        self.recent_bb = 0
        self.recent_so = 0
        self.recent_r = 0
        self.recent_sb = 0
        self.recent_cs = 0
        self.recent_hr = 0
        self.recent_rbi = 0

    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<Hitter PreGame Entry(id='%s')>" % self.rotowire_id





