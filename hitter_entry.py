from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float


class HitterEntry(Base):
    """ Class for SQL entry for a Hitter
    """
    __tablename__ = 'hitter_entries'
    
    pitch_fx_id = Column(Integer, primary_key=True)
    last_game_date = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    team = Column(String)
    batting_hand = Column(String)
    
    def __init__(self, hitter):
        """ Constructor
        :param hitter: Hitter object
        """
        self.first_name = hitter.first_name
        self.last_name = hitter.last_name
        self.pitch_fx_id = hitter.pitch_fx_id
        self.last_game_date = hitter.game_date
        self.team = hitter.team
        self.batting_hand = hitter.playing_hand
        
    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<User(name='%s %s')>" % (
                                self.FirstName, self.LastName)




