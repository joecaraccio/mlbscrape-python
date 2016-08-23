from mlb_database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class HitterEntry(Base):
    """ Class for SQL entry for a Hitter
    One-to-many relationship with PregameHitterGameEntry and PostgameHitterGameEntry
    """
    __tablename__ = 'hitter_entries'

    baseball_reference_id = Column(String)
    rotowire_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    team = Column(String)
    batting_hand = Column(String)

    game_entries = relationship("PregameHitterGameEntry", backref="hitter_entry")
    postgame_entries = relationship("PostgameHitterGameEntry", backref="hitter_entry")

    def __init__(self, first_name, last_name, rotowire_id):
        """ Constructor
        :param first_name: the first name of the player
        :param last_name: the last name of the player
        :param rotowire_id: the unique RotoWire ID for this player
        """
        self.first_name = first_name
        self.last_name = last_name
        self.rotowire_id = rotowire_id
        
    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<HitterEntry(name='%s %s')>" % (
                                self.first_name, self.last_name)





