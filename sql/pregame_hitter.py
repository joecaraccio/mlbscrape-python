
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float, or_, ForeignKeyConstraint, ForeignKey, Boolean, desc
from datetime import date, datetime
import numpy as np


class PregameHitterGameEntry(Base):
    """ Class for SQL entry for a single game played by a hitter
    Many-to-one relationship with HitterEntry
    """
    __tablename__ = 'pregame_hitter_entries'

    rotowire_id = Column(String, ForeignKey('hitter_entries.rotowire_id'), primary_key=True)
    pitcher_id = Column(String, ForeignKey('pitcher_entries.rotowire_id'))
    game_date = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)
    home_team = Column(String)
    is_home_team = Column(Boolean)
    __table_args__ = (ForeignKeyConstraint([game_date, game_time, home_team],
                                           ['game_entries.game_date', 'game_entries.game_time', 'game_entries.home_team']), {})

    predicted_draftkings_points = Column(Float)
    draftkings_salary = Column(Integer)
    primary_position = Column(String)
    secondary_position = Column(String)

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
        super(PregameHitterGameEntry, self).__init__()

        self.predicted_draftkings_points = 0
        self.draftkings_salary = 0
        self.avg_points = 0

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

    @staticmethod
    def get_pct_stat(divisor, dividend):
        try:
            return float(divisor) / float(dividend)
        except ZeroDivisionError:
            return 0

    def to_season_input_vector(self):
        return [self.get_pct_stat(self.season_h, self.season_pa),
                self.get_pct_stat(self.season_bb, self.season_pa),
                self.get_pct_stat(self.season_rbi, self.season_pa),
                self.get_pct_stat(self.season_r, self.season_pa),
                self.get_pct_stat(self.season_sb, self.season_pa),
                self.get_pct_stat(self.season_hr, self.season_pa),
                self.season_pa]

    def to_career_input_vector(self):
        return [self.get_pct_stat(self.career_h, self.career_pa),
                self.get_pct_stat(self.career_bb, self.career_pa),
                self.get_pct_stat(self.career_rbi, self.career_pa),
                self.get_pct_stat(self.career_r, self.career_pa),
                self.get_pct_stat(self.career_sb, self.career_pa),
                self.get_pct_stat(self.career_hr, self.career_pa),
                self.career_pa]

    def to_vs_input_vector(self):
        return [self.get_pct_stat(self.vs_h, self.vs_pa),
                self.get_pct_stat(self.vs_bb, self.vs_pa),
                self.get_pct_stat(self.vs_rbi, self.vs_pa),
                self.get_pct_stat(self.vs_hr, self.vs_pa),
                self.vs_pa]

    def to_vs_hand_input_vector(self):
        return [self.get_pct_stat(self.vs_hand_h, self.vs_hand_pa),
                self.get_pct_stat(self.vs_hand_bb, self.vs_hand_pa),
                self.get_pct_stat(self.vs_hand_rbi, self.vs_hand_pa),
                self.get_pct_stat(self.vs_hand_r, self.vs_hand_pa),
                self.get_pct_stat(self.vs_hand_hr, self.vs_hand_pa),
                self.vs_hand_pa]

    def to_recent_input_vector(self):
        return [self.get_pct_stat(self.recent_h, self.recent_pa),
                self.get_pct_stat(self.recent_bb, self.recent_pa),
                self.get_pct_stat(self.recent_rbi, self.recent_pa),
                self.get_pct_stat(self.recent_r, self.recent_pa),
                self.get_pct_stat(self.recent_hr, self.recent_pa),
                self.recent_pa]

    def to_input_vector(self):
        return self.to_season_input_vector() + self.to_career_input_vector() + self.to_vs_hand_input_vector() + \
               self.to_vs_input_vector() + self.to_recent_input_vector()

    def to_input_vector_raw(self):
        #TODO: this shouldn't include the totals that are returned by the corresponding to_..._vector
        input_vector = np.concatenate([np.array(self.to_season_input_vector())*self.season_pa,
        np.array(self.to_career_input_vector())*self.career_pa,
        np.array(self.to_vs_hand_input_vector())*self.vs_hand_pa,
        np.array(self.to_vs_input_vector())*self.vs_ab,
        np.array(self.to_recent_input_vector())*self.recent_ab])
        return input_vector

    @staticmethod
    def avg_input_vector(input_vector):

        if input_vector[6] != 0:
            season = np.array(input_vector[0:6]) / input_vector[6]
            season = np.append(season, input_vector[6])
        else:
            season = np.zeros(7)

        if input_vector[13] != 0:
            career = np.array(input_vector[7:13]) / input_vector[13]
            career = np.append(career, input_vector[13])
        else:
            career = np.zeros(7)

        if input_vector[19] != 0:
            vs_hand = np.array(input_vector[14:19]) / input_vector[19]
            vs_hand = np.append(vs_hand, input_vector[19])
        else:
            vs_hand = np.zeros(6)

        if input_vector[24] != 0:
            vs = np.array(input_vector[20:24]) / input_vector[24]
            vs = np.append(vs, input_vector[24])
        else:
            vs = np.zeros(5)

        if input_vector[30] != 0:
            recent = np.array(input_vector[25:30]) / input_vector[30]
            recent = np.append(recent, input_vector[30])
        else:
            recent = np.zeros(6)

        return np.concatenate([season, career, vs_hand, vs, recent])

    @staticmethod
    def get_input_vector_labels():
        return ["Season Hits / PA", "Season Walks / PA", "Season RBIs / PA", "Season Runs / PA",
                "Season SB / PA", "Season HR / PA", "Season PA",
                "Career Hits / PA", "Career Walks / PA", "Career RBIs / PA", "Career Runs / PA",
                "Career SB / PA", "Career HR / PA", "Career PA",
                "Versus Hits / PA", "Versus Walks / PA", "Versus RBIs / PA", "Versus HR / PA", "Versus PA",
                "Versus Hand Hits / PA", "Versus Hand Walks / PA", "Versus Hand RBIs / PA",
                "Versus Hand Runs / PA", "Versus Hand HR / PA", "Versus Hand PA",
                "Recent Hits / PA", "Recent Walks / PA", "Recent RBIs / PA", "Recent Runs / PA",
                "Recent HR / PA", "Recent PA"]

    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<Hitter PreGame Entry(name=%s %s, team='%s', id='%s', salary=%i, $/point=%f, points=%f)>" % \
               (self.hitter_entry.first_name,
                self.hitter_entry.last_name,
                self.hitter_entry.team,
                self.rotowire_id,
                self.draftkings_salary,
                self.dollars_per_point(),
                self.predicted_draftkings_points)

    @staticmethod
    def get_all_daily_entries(database_session, game_datetime=None):
        if game_datetime is None:
            game_datetime = datetime.now()
            game_datetime = game_datetime.replace(hour=23, minute=0, second=0)
        query = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == str(game_datetime.date()))
        if query.count() > 0:
            query = query.order_by(desc(PregameHitterGameEntry.predicted_draftkings_points))
        items = list()
        for item in query:
            if datetime.strptime(item.game_time, '%H:%M') <= game_datetime:
                items.append(item)

        return items

    @staticmethod
    def get_daily_entries_by_position(database_session, position, game_datetime=None):
        """ Get the daily pregame hitter entries by position before a certain cutoff time
        :param database_session: SQLAlchemy database session
        :param position: position abbreviation
        :param game_date: datetime object housing the day of the game and the cutoff time
        :return: SQLAlchemy query of PregameHitterGameEntry
        """
        if game_datetime is None:
            game_datetime = datetime.now()
            game_datetime = game_datetime.replace(hour=23, minute=0, second=0)
        query = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == str(game_datetime.date()),
                                                                      or_(PregameHitterGameEntry.primary_position == position,
                                                                      PregameHitterGameEntry.secondary_position == position))
        if query.count() > 0:
            query = query.order_by(desc(PregameHitterGameEntry.predicted_draftkings_points))
        items = list()
        for item in query:
            if datetime.strptime(item.game_time, '%H:%M') <= game_datetime:
                items.append(item)

        return items

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