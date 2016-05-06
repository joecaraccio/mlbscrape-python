
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float
from datetime import date


class InfoVars(object):
    rotowire_id = Column(String, primary_key=True)
    pitcher_id = Column(String)
    game_date = Column(String, primary_key=True)
    team = Column(String)
    opposing_team = Column(String)
    predicted_draftkings_points = Column(Float)
    draftkings_salary = Column(Integer)
    primary_position = Column(String)
    secondary_position = Column(String)

    def __init__(self):
        super(InfoVars, self).__init__()
        self.predicted_draftkings_points = 0
        self.draftkings_salary = 0


class DataVars(object):
    # Season stats
    season_pa = Column(Integer)
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
    career_pa = Column(Integer)
    career_ab = Column(Integer)
    career_h = Column(Integer)
    career_bb = Column(Integer)
    career_so = Column(Integer)
    career_r = Column(Integer)
    career_sb = Column(Integer)
    career_cs = Column(Integer)
    career_hr = Column(Integer)
    career_rbi = Column(Integer)

    # Versus the opposing pitcher
    vs_pa = Column(Integer)
    vs_ab = Column(Integer)
    vs_h = Column(Integer)
    vs_bb = Column(Integer)
    vs_so = Column(Integer)
    vs_hr = Column(Integer)
    vs_rbi = Column(Integer)

    # Versus the hand of the opposing pitcher
    vs_hand_pa = Column(Integer)
    vs_hand_ab = Column(Integer)
    vs_hand_h = Column(Integer)
    vs_hand_bb = Column(Integer)
    vs_hand_so = Column(Integer)
    vs_hand_r = Column(Integer)
    vs_hand_sb = Column(Integer)
    vs_hand_cs = Column(Integer)
    vs_hand_hr = Column(Integer)
    vs_hand_rbi = Column(Integer)

    # Recent stats
    recent_pa = Column(Integer)
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
        super(DataVars, self).__init__()
        # Season stats
        self.season_pa = 0
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
        self.career_pa = 0
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
        self.vs_pa = 0
        self.vs_ab = 0
        self.vs_h = 0
        self.vs_bb = 0
        self.vs_so = 0
        self.vs_hr = 0
        self.vs_rbi = 0

        self.vs_hand_pa = 0
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
        self.recent_pa = 0
        self.recent_ab = 0
        self.recent_h = 0
        self.recent_bb = 0
        self.recent_so = 0
        self.recent_r = 0
        self.recent_sb = 0
        self.recent_cs = 0
        self.recent_hr = 0
        self.recent_rbi = 0


class PregameHitterGameEntry(InfoVars, DataVars, Base):
    """ Class for SQL entry for a single game played by a hitter
    """
    __tablename__ = 'pregame_hitter_entries'

    def __init__(self):
        super(PregameHitterGameEntry, self).__init__()

    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<Hitter PreGame Entry(id='%s')>" % self.rotowire_id

    def to_vector(self):
        """ Convert the entry to a vector
        :return: a list representation of the entry
        """
        vector = list()
        for variable in vars(self):
            if variable in vars(DataVars):
                vector.append(self.__dict__[variable])

        print vector

        return vector





