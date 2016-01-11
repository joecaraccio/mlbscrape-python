
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float

# Baseball player class
class HitterEntry(Base):
    __tablename__ = 'game_entries'
    
    #mPitchFxId = Column(Integer, Sequence('hitter_id_seq'), primary_key=True)
    mPitchFxId = Column(Integer, primary_key=True)
    mGameId = Column(String,primary_key=True)
    mDraftKingsPoints = Column(Float)
    mFirstName = Column(String)
    mLastName = Column(String)
    
    # Season stats
    mSeasonAb = Column(Float)
    mSeasonH = Column(Float)
    mSeasonBb = Column(Float)
    mSeasonSo = Column(Float)
    mSeasonR = Column(Float)
    mSeasonSb = Column(Float)
    mSeasonCs = Column(Float)
    mSeasonHr = Column(Float)
    mSeasonRbi = Column(Float)
    mSeasonOps = Column(Float)
    
    # Career stats
    mCareerAb = Column(Float)
    mCareerH = Column(Float)
    mCareerBb = Column(Float)
    mCareerSo = Column(Float)
    mCareerR = Column(Float)
    mCareerSb = Column(Float)
    mCareerCs = Column(Float)
    mCareerHr = Column(Float)
    mCareerRbi = Column(Float)
    mCareerOps = Column(Float)
    
    # Versus stats
    mVsAb = Column(Float)
    mVsH = Column(Float)
    mVsBb = Column(Float)
    mVsSo = Column(Float)
    mVsR = Column(Float)
    mVsSb = Column(Float)
    mVsCs = Column(Float)
    mVsHr = Column(Float)
    mVsRbi = Column(Float)
    mVsOps = Column(Float)
    
    def __init__(self,hitter):
        self.mFirstName = hitter.mFirstName
        self.mLastName = hitter.mLastName
        self.mPitchFxId = hitter.mPitchFxId
        self.mGameId = hitter.mGameId
        
        self.mDraftKingsPoints = hitter.mTotalPoints
        
        # Season stats
        self.mSeasonAb = hitter.mSeasonAb
        self.mSeasonH = hitter.mSeasonH
        self.mSeasonBb = hitter.mSeasonBb
        self.mSeasonSo = hitter.mSeasonSo
        self.mSeasonR = hitter.mSeasonR
        self.mSeasonSb = hitter.mSeasonSb
        self.mSeasonCs = hitter.mSeasonCs
        self.mSeasonHr = hitter.mSeasonHr
        self.mSeasonRbi = hitter.mSeasonRbi
        self.mSeasonOps = hitter.mSeasonOps
        
        # Career stats
        self.mCareerAb = hitter.mCareerAb
        self.mCareerH = hitter.mCareerH
        self.mCareerBb = hitter.mCareerBb
        self.mCareerSo = hitter.mCareerSo
        self.mCareerR = hitter.mCareerR
        self.mCareerSb = hitter.mCareerSb
        self.mCareerCs = hitter.mCareerCs
        self.mCareerHr = hitter.mCareerHr
        self.mCareerRbi = hitter.mCareerRbi
        self.mCareerOps = hitter.mCareerOps
        
        # Versus stats
        self.mVsAb = hitter.mVsAb
        self.mVsH = hitter.mVsH
        self.mVsBb = hitter.mVsBb
        self.mVsSo = hitter.mVsSo
        self.mVsR = hitter.mVsR
        self.mVsSb = hitter.mVsSb
        self.mVsCs = hitter.mVsCs
        self.mVsHr = hitter.mVsHr
        self.mVsRbi = hitter.mVsRbi
        self.mVsOps = hitter.mVsOps
        
    def __repr__(self):
        return "<User(name='%s %s')>" % (
                                self.mFirstName, self.mLastName)




