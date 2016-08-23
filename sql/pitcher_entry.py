from sqlalchemy import Column, String
from mlb_database import Base
from sqlalchemy.orm import relationship


class PitcherEntry(Base):
    """ Class for Pitcher entries into an SQL database
    One-to-many relationship with PregamePitcherGameEntry and PostgamePitcherGameEntry
    """
    __tablename__ = 'pitcher_entries'

    baseball_reference_id = Column(String)
    rotowire_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    team = Column(String)
    pitching_hand = Column(String)

    game_entries = relationship("PregamePitcherGameEntry", backref="pitcher_entry")
    postgame_entries = relationship("PostgamePitcherGameEntry", backref="pitcher_entry")

    def __init__(self, first_name, last_name, rotowire_id):
        """ Constructor
        :param pitcher: Pitcher object
        """
        self.first_name = first_name
        self.last_name = last_name
        self.rotowire_id = rotowire_id
        
    def __repr__(self):
        return "<PitcherEntry(name='%s %s')>" % (
                                self.first_name, self.last_name)





