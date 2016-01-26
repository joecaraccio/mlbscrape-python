
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
    
    # Game stats
    SeasonAb = Column(Integer)
    GameH = Column(Integer)
    GameBb = Column(Integer)
    GameSo = Column(Integer)
    GameR = Column(Integer)
    GameSb = Column(Integer)
    GameCs = Column(Integer)
    GameHr = Column(Integer)
    GameRbi = Column(Integer)
    
    # Season stats
    SeasonAb = Column(Integer)
    SeasonH = Column(Integer)
    SeasonBb = Column(Integer)
    SeasonSo = Column(Integer)
    SeasonR = Column(Integer)
    SeasonSb = Column(Integer)
    SeasonCs = Column(Integer)
    SeasonHr = Column(Integer)
    SeasonRbi = Column(Integer)
    
    # Career stats
    CareerAb = Column(Integer)
    CareerH = Column(Integer)
    CareerBb = Column(Integer)
    CareerSo = Column(Integer)
    CareerR = Column(Integer)
    CareerSb = Column(Integer)
    CareerCs = Column(Integer)
    CareerHr = Column(Integer)
    CareerRbi = Column(Integer)
    
    # Versus stats
    VsAb = Column(Integer)
    VsH = Column(Integer)
    VsBb = Column(Integer)
    VsSo = Column(Integer)
    VsR = Column(Integer)
    VsSb = Column(Integer)
    VsCs = Column(Integer)
    VsHr = Column(Integer)
    VsRbi = Column(Integer)
    
    # Month stats
    MonthAb = Column(Integer)
    MonthH = Column(Integer)
    MonthBb = Column(Integer)
    MonthSo = Column(Integer)
    MonthR = Column(Integer)
    MonthSb = Column(Integer)
    MonthCs = Column(Integer)
    MonthHr = Column(Integer)
    MonthRbi = Column(Integer)
    
    def __init__(self,hitter):
        self.FirstName = hitter.mFirstName
        self.LastName = hitter.mLastName
        self.PitchFxId = hitter.mPitchFxId
        self.GameId = hitter.mGameId
        self.Team = hitter.mTeamAbbrev
        self.DraftKingsPoints = hitter.mTotalPoints
        self.BattingOrder = hitter.mBattingOrder
        self.GameDate = hitter.mGameDate
        
        # Game stats
        self.GameAb = hitter.mGameAb
        self.GameH = hitter.mGameH
        self.GameBb = hitter.mGameBb
        self.GameSo = hitter.mGameSo
        self.GameR = hitter.mGameR
        self.GameSb = hitter.mGameSb
        self.GameCs = hitter.mGameCs
        self.GameHr = hitter.mGameHr
        self.GameRbi = hitter.mGameRbi
        
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
        
    def __repr__(self):
        return "<User(name='%s %s')>" % (
                                self.FirstName, self.LastName)




