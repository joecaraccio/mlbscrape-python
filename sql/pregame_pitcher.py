from sqlalchemy import Column, Integer, String, Float
from datetime import date
from mlb_database import Base


class InfoVars(object):
    """ Class for informational variables for a pitcher's pregame
    """
    rotowire_id = Column(String, primary_key=True)
    team = Column(String)
    game_date = Column(String, primary_key=True)
    opposing_team = Column(String)
    predicted_draftkings_points = Column(Float)
    draftkings_salary = Column(Integer)

    def __init__(self):
        super(InfoVars, self).__init__()
        self.predicted_draftkings_points = 0
        self.draftkings_salary = 0


class DataVars(object):
    """ Class for data variables for a pitcher's pregame
    """
    # Season stats
    season_bf = Column(Integer)
    season_ip = Column(Float)
    season_so = Column(Integer)
    season_wins = Column(Integer)
    season_losses = Column(Integer)
    season_er = Column(Integer)
    season_h = Column(Integer)
    season_bb = Column(Integer)
    season_hr = Column(Integer)

    # Career stats
    career_bf = Column(Integer)
    career_ip = Column(Float)
    career_so = Column(Integer)
    career_wins = Column(Integer)
    career_losses = Column(Integer)
    career_er = Column(Integer)
    career_h = Column(Integer)
    career_bb = Column(Integer)
    career_hr = Column(Integer)

    # Versus stats
    vs_bf = Column(Integer)
    vs_so = Column(Integer)
    vs_er = Column(Integer)
    vs_h = Column(Integer)
    vs_bb = Column(Integer)
    vs_hr = Column(Integer)

    # Recent (last 14 days) stats
    recent_bf = Column(Integer)
    recent_ip = Column(Float)
    recent_so = Column(Integer)
    recent_er = Column(Integer)
    recent_h = Column(Integer)
    recent_bb = Column(Integer)
    recent_hr = Column(Integer)

    def __init__(self):
        super(DataVars, self).__init__()

        # Season stats
        self.season_bf = 0
        self.season_ip = 0
        self.season_so = 0
        self.season_wins = 0
        self.season_losses = 0
        self.season_er = 0
        self.season_h = 0
        self.season_bb = 0
        self.season_hr = 0

        # Career stats
        self.career_bf = 0
        self.career_ip = 0
        self.career_so = 0
        self.career_wins = 0
        self.career_losses = 0
        self.career_er = 0
        self.career_h = 0
        self.career_bb = 0
        self.career_hr = 0

        # Versus stats
        self.vs_bf = 0
        self.vs_so = 0
        self.vs_er = 0
        self.vs_h = 0
        self.vs_bb = 0
        self.vs_hr = 0

        # Month stats
        self.recent_bf = 0
        self.recent_ip = 0
        self.recent_so = 0
        self.recent_er = 0
        self.recent_h = 0
        self.recent_bb = 0
        self.recent_hr = 0


class PregamePitcherGameEntry(InfoVars, DataVars, Base):

    __tablename__ = 'pregame_pitcher_entries'
    
    def __init__(self):
        """ Constructor
        Copy the Pitcher object into the PitcherGameEntry fields
        :param pitcher: Pitcher object
        """
        super(PregamePitcherGameEntry, self).__init__()
        
    def __repr__(self):
        """
        :return: string representation identifying the Pitcher entry
        """
        return "<Pitcher game entry(name='%s')>" % self.rotowire_id

    def to_vector(self):
        """ Convert the entry to a vector
        :return: a list representation of the entry
        """
        vector = list()
        for variable in vars(self):
            if variable in vars(DataVars):
                vector.append(self.__dict__[variable])

        return vector

    @staticmethod
    def get_all_daily_entries(database_session, game_date=None):
        if game_date is None:
            game_date = date.today()
        return database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == game_date)




