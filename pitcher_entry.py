from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float

# Entry for the Hitter database which has a link to the last game mined
class PitcherEntry(Base):
    __tablename__ = 'pitcher_entries'
    
    PitchFxId = Column(Integer, primary_key=True)
    LastGameDate = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Team = Column(String)
    PitchingHand = Column(String)
    
    def __init__(self,pitcher):
        self.FirstName = pitcher.mFirstName
        self.LastName = pitcher.mLastName
        self.PitchFxId = pitcher.mPitchFxId
        self.LastGameDate = pitcher.mGameDate
        self.Team = pitcher.mTeamAbbrev
        self.PitchingHand = pitcher.mPlayingHand
        
    def __repr__(self):
        return "<User(name='%s %s')>" % (
                                self.FirstName, self.LastName)




