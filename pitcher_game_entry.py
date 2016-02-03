
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float

# Baseball player class
class PitcherGameEntry(Base):
    __tablename__ = 'pitcher_game_entries'
    
    PitchFxId = Column(Integer, primary_key=True)
    GameId = Column(String,primary_key=True)
    DraftKingsPoints = Column(Float)
    FirstName = Column(String)
    LastName = Column(String)
    Team = Column(String)
    GameDate = Column(String)
    
    # Game stats
    GameOuts = Column(Integer)
    GameSo = Column(Integer)
    GameW = Column(Integer)
    GameL = Column(Integer)
    GameEr = Column(Integer)
    GameH = Column(Integer)
    GameBb = Column(Integer)
    GameHr = Column(Integer)
    
    # Season stats
    SeasonOuts = Column(Integer)
    SeasonSo = Column(Integer)
    SeasonW = Column(Integer)
    SeasonL = Column(Integer)
    SeasonEr = Column(Integer)
    SeasonH = Column(Integer)
    SeasonBb = Column(Integer)
    SeasonHr = Column(Integer)
    
    # Career stats
    CareerOuts = Column(Integer)
    CareerSo = Column(Integer)
    CareerW = Column(Integer)
    CareerL = Column(Integer)
    CareerEr = Column(Integer)
    CareerH = Column(Integer)
    CareerBb = Column(Integer)
    CareerHr = Column(Integer)
    
    # Versus stats
    VsOuts = Column(Float)
    VsSo = Column(Integer)
    VsEr = Column(Integer)
    VsH = Column(Integer)
    VsBb = Column(Integer)
    VsHr = Column(Integer)
    VsLhbOuts = Column(Float)
    VsLhbSo = Column(Integer)
    VsLhbEr = Column(Integer)
    VsLhbH = Column(Integer)
    VsLhbBb = Column(Integer)
    VsLhbHr = Column(Integer)
    VsRhbOuts = Column(Float)
    VsRhbSo = Column(Integer)
    VsRhbEr = Column(Integer)
    VsRhbH = Column(Integer)
    VsRhbBb = Column(Integer)
    VsRhbHr = Column(Integer)
    
    # Month stats
    MonthOuts = Column(Integer)
    MonthSo = Column(Integer)
    MonthEr = Column(Integer)
    MonthH = Column(Integer)
    MonthBb = Column(Integer)
    MonthHr = Column(Integer)
    
    def __init__(self,pitcher):
        self.FirstName = pitcher.mFirstName
        self.LastName = pitcher.mLastName
        self.PitchFxId = pitcher.mPitchFxId
        self.GameId = pitcher.mGameId
        self.Team = pitcher.mTeamAbbrev
        self.DraftKingsPoints = pitcher.mTotalPoints
        self.GameDate = pitcher.mGameDate
        
        # Game stats
        self.GameOuts = pitcher.mGameOuts
        self.GameSo = pitcher.mGameSo
        self.GameW = pitcher.mGameW
        self.GameL = pitcher.mGameL
        self.GameEr = pitcher.mGameEr
        self.GameH = pitcher.mGameH
        self.GameBb = pitcher.mGameBb
        self.GameHr = pitcher.mGameHr
        
        # Season stats
        self.SeasonOuts = pitcher.mSeasonOuts
        self.SeasonSo = pitcher.mSeasonSo
        self.SeasonW = pitcher.mSeasonW
        self.SeasonL = pitcher.mSeasonL
        self.SeasonEr = pitcher.mSeasonEr
        self.SeasonH = pitcher.mSeasonH
        self.SeasonBb = pitcher.mSeasonBb
        self.SeasonHr = pitcher.mSeasonHr
        
        # Career stats
        self.CareerOuts = pitcher.mCareerOuts
        self.CareerSo = pitcher.mCareerSo
        self.CareerW = pitcher.mCareerW
        self.CareerL = pitcher.mCareerL
        self.CareerEr = pitcher.mCareerEr
        self.CareerH = pitcher.mCareerH
        self.CareerBb = pitcher.mCareerBb
        self.CareerHr = pitcher.mCareerHr
        
        # Versus stats
        self.VsOuts = pitcher.mVsOuts
        self.VsSo = pitcher.mVsSo
        self.VsEr = pitcher.mVsEr
        self.VsH = pitcher.mVsH
        self.VsBb = pitcher.mVsBb
        self.VsHr = pitcher.mVsHr
        self.VsLhbOuts = pitcher.mVsLhbOuts
        self.VsLhbSo = pitcher.mVsLhbSo
        self.VsLhbEr = pitcher.mVsLhbEr
        self.VsLhbH = pitcher.mVsLhbH
        self.VsLhbBb = pitcher.mVsLhbBb
        self.VsLhbHr = pitcher.mVsLhbHr
        self.VsRhbOuts = pitcher.mVsRhbOuts
        self.VsRhbSo = pitcher.mVsRhbSo
        self.VsRhbEr = pitcher.mVsRhbEr
        self.VsRhbH = pitcher.mVsRhbH
        self.VsRhbBb = pitcher.mVsRhbBb
        self.VsRhbHr = pitcher.mVsRhbHr
        
        # Month stats
        self.MonthOuts = pitcher.mMonthOuts
        self.MonthSo = pitcher.mMonthSo
        self.MonthEr = pitcher.mMonthEr
        self.MonthH = pitcher.mMonthH
        self.MonthBb = pitcher.mMonthBb
        self.MonthHr = pitcher.mMonthHr
        
    def __repr__(self):
        return "<User(name='%s %s')>" % (
                                self.FirstName, self.LastName)




