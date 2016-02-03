from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float

# Entry for the Hitter database which has a link to the last game mined
class HitterEntry(Base):
    __tablename__ = 'hitter_entries'
    
    PitchFxId = Column(Integer, primary_key=True)
    LastGameDate = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Team = Column(String)
    BattingHand = Column(String)
    
    def __init__(self,hitter):
        self.FirstName = hitter.mFirstName
        self.LastName = hitter.mLastName
        self.PitchFxId = hitter.mPitchFxId
        self.LastGameDate = hitter.mGameDate
        self.Team = hitter.mTeamAbbrev
        self.BattingHand = hitter.mPlayingHand
        
    def __repr__(self):
        return "<User(name='%s %s')>" % (
                                self.FirstName, self.LastName)




