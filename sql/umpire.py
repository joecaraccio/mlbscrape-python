from mlb_database import Base
from sqlalchemy import Column, String, Float
import numpy as np


class UmpireCareerEntry(Base):
    """ Class for SQL entry for a Hitter
    One-to-many relationship with PregameHitterGameEntry and PostgameHitterGameEntry
    """
    __tablename__ = 'umpire_entries'

    full_name = Column(String, primary_key=True)

    ks_pct = Column(Float)
    walks_pct = Column(Float)
    runs_per_game = Column(Float)
    batting_average = Column(Float)
    on_base_pct = Column(Float)
    slugging_pct = Column(Float)

    ks_boost = Column(Float)
    walks_boost = Column(Float)
    runs_boost = Column(Float)
    batting_average_boost = Column(Float)
    on_base_pct_boost = Column(Float)
    slugging_pct_boost = Column(Float)

    def __init__(self, full_name):
        """ Constructor
        :param first_name: the first name of the player
        :param last_name: the last name of the player
        :param rotowire_id: the unique RotoWire ID for this player
        """
        self.full_name = full_name

    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<UmpireCareerEntry(name='%s %s')>" % self.full_name

    def to_input_vector(self):
        return np.array([self.ks_pct, self.walks_pct, self.runs_per_game, self.batting_average,
                         self.on_base_pct, self.slugging_pct, self.ks_boost, self.walks_boost,
                         self.runs_boost, self.batting_average_boost, self.on_base_pct_boost,
                         self.slugging_pct_boost])

    @staticmethod
    def get_nominal_data(database_session):
        """ Average all of the umpire data to use when we don't know the ump's name
        :return: numpy array representing the umpire stats
        """
        ump_entries = database_session.query(UmpireCareerEntry)
        ks_pct = 0.0
        walks_pct = 0.0
        runs_per_game = 0.0
        batting_average = 0.0
        on_base_pct = 0.0
        slugging_pct = 0.0
        ks_boost = 0.0
        walks_boost = 0.0
        runs_boost = 0.0
        batting_average_boost = 0.0
        on_base_pct_boost = 0.0
        slugging_pct_boost = 0.0

        for ump_entry in ump_entries:
            ks_pct += ump_entry.ks_pct
            walks_pct += ump_entry.walks_pct
            runs_per_game += ump_entry.runs_per_game
            batting_average += ump_entry.batting_average
            on_base_pct += ump_entry.on_base_pct
            slugging_pct += ump_entry.slugging_pct
            ks_boost += ump_entry.ks_boost
            walks_boost += ump_entry.walks_boost
            runs_boost += ump_entry.runs_boost
            batting_average_boost += ump_entry.batting_average_boost
            on_base_pct_boost += ump_entry.on_base_pct_boost
            slugging_pct_boost += ump_entry.slugging_pct_boost

        ks_pct /= ump_entries.count()
        walks_pct /= ump_entries.count()
        runs_per_game /= ump_entries.count()
        batting_average /= ump_entries.count()
        on_base_pct /= ump_entries.count()
        slugging_pct /= ump_entries.count()
        ks_boost /= ump_entries.count()
        walks_boost /= ump_entries.count()
        runs_boost /= ump_entries.count()
        batting_average_boost /= ump_entries.count()
        on_base_pct_boost /= ump_entries.count()
        slugging_pct_boost /= ump_entries.count()

        return np.array([ks_pct, walks_pct, runs_per_game, batting_average,
                         on_base_pct, slugging_pct, ks_boost, walks_boost,
                         runs_boost, batting_average_boost, on_base_pct_boost,
                         slugging_pct_boost])



