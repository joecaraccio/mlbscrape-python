
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float

# Baseball player class
class HitterGameEntry(Base):
    __tablename__ = 'hitter_game_entries'
    
    PitchFxId = Column(Integer, primary_key=True)
    GameId = Column(String,primary_key=True)
    DraftKingsPoints = Column(Float)
    FirstName = Column(String)
    LastName = Column(String)
    Team = Column(String)
    BattingOrder = Column(Integer)
    GameDate = Column(String)
    
    # Season stats
    SeasonAb = Column(Float)
    SeasonH = Column(Float)
    SeasonBb = Column(Float)
    SeasonSo = Column(Float)
    SeasonR = Column(Float)
    SeasonSb = Column(Float)
    SeasonCs = Column(Float)
    SeasonHr = Column(Float)
    SeasonRbi = Column(Float)
    SeasonOps = Column(Float)
    
    # Career stats
    CareerAb = Column(Float)
    CareerH = Column(Float)
    CareerBb = Column(Float)
    CareerSo = Column(Float)
    CareerR = Column(Float)
    CareerSb = Column(Float)
    CareerCs = Column(Float)
    CareerHr = Column(Float)
    CareerRbi = Column(Float)
    CareerOps = Column(Float)
    
    # Versus stats
    VsAb = Column(Float)
    VsH = Column(Float)
    VsBb = Column(Float)
    VsSo = Column(Float)
    VsR = Column(Float)
    VsSb = Column(Float)
    VsCs = Column(Float)
    VsHr = Column(Float)
    VsRbi = Column(Float)
    VsOps = Column(Float)
    
    # Month stats
    MonthAb = Column(Float)
    MonthH = Column(Float)
    MonthBb = Column(Float)
    MonthSo = Column(Float)
    MonthR = Column(Float)
    MonthSb = Column(Float)
    MonthCs = Column(Float)
    MonthHr = Column(Float)
    MonthRbi = Column(Float)
    MonthOps = Column(Float)
    
    def __init__(self,hitter):
        self.FirstName = hitter.mFirstName
        self.LastName = hitter.mLastName
        self.PitchFxId = hitter.mPitchFxId
        self.GameId = hitter.mGameId
        self.Team = hitter.mTeamAbbrev
        self.DraftKingsPoints = hitter.mTotalPoints
        self.BattingOrder = hitter.mBattingOrder
        self.GameDate = hitter.mGameDate
        
        # Season stats
        self.SeasonAb = hitter.mSeasonAb
        self.SeasonH = hitter.mSeasonH
        self.SeasonBb = hitter.mSeasonBb
        self.SeasonSo = hitter.mSeasonSo
        self.SeasonR = hitter.mSeasonR
        self.SeasonSb = hitter.mSeasonSb
        self.SeasonCs = hitter.mSeasonCs
        self.SeasonHr = hitter.mSeasonHr
        self.SeasonRbi = hitter.mSeasonRbi
        self.SeasonOps = hitter.mSeasonOps
        
        # Career stats
        self.CareerAb = hitter.mCareerAb
        self.CareerH = hitter.mCareerH
        self.CareerBb = hitter.mCareerBb
        self.CareerSo = hitter.mCareerSo
        self.CareerR = hitter.mCareerR
        self.CareerSb = hitter.mCareerSb
        self.CareerCs = hitter.mCareerCs
        self.CareerHr = hitter.mCareerHr
        self.CareerRbi = hitter.mCareerRbi
        self.CareerOps = hitter.mCareerOps
        
        # Versus stats
        self.VsAb = hitter.mVsAb
        self.VsH = hitter.mVsH
        self.VsBb = hitter.mVsBb
        self.VsSo = hitter.mVsSo
        self.VsR = hitter.mVsR
        self.VsSb = hitter.mVsSb
        self.VsCs = hitter.mVsCs
        self.VsHr = hitter.mVsHr
        self.VsRbi = hitter.mVsRbi
        self.VsOps = hitter.mVsOps
        
        # Month stats
        self.MonthAb = hitter.mMonthAb
        self.MonthH = hitter.mMonthH
        self.MonthBb = hitter.mMonthBb
        self.MonthSo = hitter.mMonthSo
        self.MonthR = hitter.mMonthR
        self.MonthSb = hitter.mMonthSb
        self.MonthCs = hitter.mMonthCs
        self.MonthHr = hitter.mMonthHr
        self.MonthRbi = hitter.mMonthRbi
        self.MonthOps = hitter.mMonthOps
        
    def __repr__(self):
        return "<User(name='%s %s')>" % (
                                self.FirstName, self.LastName)




