from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float


class PitcherEntry(Base):
    """ Class for Pitcher entries into an SQL database
    """
    __tablename__ = 'pitcher_entries'
    
    pitch_fx_id = Column(Integer, primary_key=True)
    last_game_date = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    team = Column(String)
    pitching_hand = Column(String)
    
    def __init__(self, pitcher):
        """ Constructor
        :param pitcher: Pitcher object
        """
        self.first_name = pitcher.first_name
        self.last_name = pitcher.last_name
        self.pitch_fx_id = pitcher.pitch_fx_id
        self.last_game_date = pitcher.game_date
        self.team = pitcher.team
        self.pitching_hand = pitcher.playing_hand
        
    def __repr__(self):
        return "<User(name='%s %s')>" % (
                                self.FirstName, self.LastName)




