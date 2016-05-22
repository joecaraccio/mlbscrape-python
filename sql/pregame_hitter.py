
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float
from datetime import date
from sqlalchemy import or_
import time


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

    def to_input_vector(self):
        return [self.season_pa, self.season_ab, self.season_h, self.season_bb, self.season_so, self.season_r, self.season_sb,
                self.season_cs, self.season_hr, self.season_rbi,
                self.career_pa, self.career_ab, self.career_h, self.career_bb, self.career_so, self.career_r, self.career_sb,
                self.career_cs, self.career_hr, self.career_rbi,
                self.vs_pa, self.vs_ab, self.vs_h, self.vs_bb, self.vs_so, self.vs_hr, self.vs_rbi,
                self.vs_hand_pa, self.vs_hand_ab, self.vs_hand_h, self.vs_hand_bb, self.vs_hand_so, self.vs_hand_r,
                self.vs_hand_sb, self.vs_hand_cs, self.vs_hand_hr, self.vs_hand_rbi,
                self.recent_pa, self.recent_ab, self.recent_h, self.recent_bb, self.recent_so, self.recent_r,
                self.recent_sb, self.recent_cs, self.recent_hr, self.recent_rbi]


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
        return "<Hitter PreGame Entry(id='%s', salary=%i, predicted_points=%f)>" % (self.rotowire_id,
                                                                                    self.draftkings_salary,
                                                                                    self.predicted_draftkings_points)

    @staticmethod
    def get_all_daily_entries(database_session, game_date=None):
        if game_date is None:
            game_date = date.today()
        return database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == game_date)

    @staticmethod
    def get_daily_entries_by_position(database_session, position, game_date=None):
        if game_date is None:
            game_date = date.today()
        return database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == game_date,
                                                                     or_(PregameHitterGameEntry.primary_position == position,
                                                                     PregameHitterGameEntry.secondary_position == position))



