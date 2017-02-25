from mlb_database import Base
from sqlalchemy import Column, String, Float


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





