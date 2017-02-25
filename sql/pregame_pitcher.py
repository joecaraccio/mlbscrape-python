from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from mlb_database import Base
from pregame_hitter import PregameHitterGameEntry
import numpy as np
from sql.mlb_database import MlbDatabase


class PregamePitcherGameEntry(Base):

    __tablename__ = 'pregame_pitcher_entries'

    rotowire_id = Column(String, ForeignKey('pitcher_entries.rotowire_id'), primary_key=True)
    game_date = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)
    home_team = Column(String)
    is_home_team = Column(Boolean)
    __table_args__ = (ForeignKeyConstraint([game_date, game_time, home_team],
                                           ['game_entries.game_date', 'game_entries.game_time', 'game_entries.home_team']), {})
    predicted_draftkings_points = Column(Float)
    draftkings_salary = Column(Integer)
    avg_points = Column(Float)

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
        """ Constructor
        Copy the Pitcher object into the PitcherGameEntry fields
        :param pitcher: Pitcher object
        """
        super(PregamePitcherGameEntry, self).__init__()

        self.predicted_draftkings_points = 0
        self.draftkings_salary = 0
        self.avg_points = 0

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
        
    def __repr__(self):
        """
        :return: string representation identifying the Pitcher entry
        """
        return "<Pitcher PreGame Entry(name=%s %s, team='%s', id='%s', salary=%i, $/point=%f, points=%f, avg_points=%f)>" %\
               (self.pitcher_entry.first_name,
                self.pitcher_entry.last_name,
                self.pitcher_entry.team,
                self.rotowire_id,
                self.draftkings_salary,
                self.dollars_per_point(),
                self.predicted_draftkings_points,
                self.avg_points)

    def to_input_vector(self):
        """ Convert the entry to a vector
        :return: a list representation of the entry
        """
        return [self.season_bf, self.season_ip, self.season_so, self.season_wins, self.season_losses, self.season_er,
                self.season_h, self.season_bb, self.season_hr,
                self.career_bf, self.career_ip, self.career_so, self.career_wins, self.career_losses, self.career_er,
                self.career_h, self.career_bb, self.career_hr,
                self.vs_bf, self.vs_so, self.vs_er, self.vs_h, self.vs_bb, self.vs_hr,
                self.recent_bf, self.recent_ip, self.recent_so, self.recent_er, self.recent_h, self.recent_bb,
                self.recent_hr]

    def get_opponent_vector(self):

        database_session = MlbDatabase().open_session()
        # Get the hitters he is facing as well
        hitter_postgame_entries = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.team == self.opposing_team,
                                                                                        PregameHitterGameEntry.game_date == self.game_date,
                                                                                        PregameHitterGameEntry.game_time == self.game_time)

        hitter_array = np.array(np.zeros(31))
        for hitter_entry in hitter_postgame_entries:
            hitter_array += hitter_entry.to_input_vector_raw()

        database_session.close()

        return PregameHitterGameEntry.avg_input_vector(hitter_array)

    @staticmethod
    def get_input_vector_labels():
        return ["Season Batters Faced", "Season IP", "Season SO", "Season Wins", "Season Losses", "Season ER",
                "Season Hits", "Season Walks", "Season HR",
                "Career Batters Faced", "Career IP", "Career SO", "Career Wins", "Career Losses", "Career ER",
                "Career Hits", "Career Walks", "Career HR",
                "Versus Batters Faced", "Versus SO", "Versus ER", "Versus Hits", "Versus Walks", "Versus HR",
                "Recent Batters Faced", "Recent IP", "Recent SO", "Recent ER", "Recent Hits", "Recent Walks",
                "Recent HR"]

    @staticmethod
    def get_all_daily_entries(database_session, game_date=None):
        if game_date is None:
            game_date = date.today()
        return database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == game_date)

    def points_per_dollar(self):
        """ Calculate the predicted points per dollar for this player.
        Return 0 if the Draftkings salary is equal to zero
        :param sql_player: a SQLAlchemy player object
        :return: float representing the predicted points per dollar
        """
        if float(self.draftkings_salary) == 0.0:
            return 0.0

        return float(self.predicted_draftkings_points) / float(self.draftkings_salary)

    def dollars_per_point(self):
        """ Calculate the predicted points per dollar for this player.
        Return 0 if the Draftkings salary is equal to zero
        :param sql_player: a SQLAlchemy player object
        :return: float representing the predicted points per dollar
        """
        if float(self.predicted_draftkings_points) == 0.0:
            return 0.0

        return float(self.draftkings_salary) / float(self.predicted_draftkings_points)

    def get_team(self):
        if self.is_home_team:
            return self.game_entry.home_team
        else:
            return self.game_entry.away_team

    def get_opposing_team(self):
        if self.is_home_team:
            return self.game_entry.away_team
        else:
            return self.game_entry.home_team