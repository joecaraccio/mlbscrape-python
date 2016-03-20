
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float

# Baseball player class
class PitcherGameEntry(Base):
    __tablename__ = 'pitcher_game_entries'
    
    pitch_fx_id = Column(String, primary_key=True)
    game_id = Column(String,primary_key=True)
    draft_kings_points = Column(Float)
    first_name = Column(String)
    last_name = Column(String)
    team = Column(String)
    game_date = Column(String)
    
    # Game stats
    game_outs = Column(Integer)
    game_so = Column(Integer)
    game_wins = Column(Integer)
    game_losses = Column(Integer)
    game_er = Column(Integer)
    game_h = Column(Integer)
    game_bb = Column(Integer)
    game_hr = Column(Integer)
    
    # Season stats
    season_outs = Column(Integer)
    season_so = Column(Integer)
    season_wins = Column(Integer)
    season_losses = Column(Integer)
    season_er = Column(Integer)
    season_h = Column(Integer)
    season_bb = Column(Integer)
    season_hr = Column(Integer)
    
    # Career stats
    career_outs = Column(Integer)
    career_so = Column(Integer)
    career_wins = Column(Integer)
    career_losses = Column(Integer)
    career_er = Column(Integer)
    career_h = Column(Integer)
    career_bb = Column(Integer)
    career_hr = Column(Integer)
    
    # Versus stats
    vs_outs = Column(Float)
    vs_so = Column(Integer)
    vs_er = Column(Integer)
    vs_h = Column(Integer)
    vs_bb = Column(Integer)
    vs_hr = Column(Integer)
    vs_lhb_outs = Column(Float)
    vs_lhb_so = Column(Integer)
    vs_lhb_er = Column(Integer)
    vs_lhb_h = Column(Integer)
    vs_lhb_bb = Column(Integer)
    vs_lhb_hr = Column(Integer)
    vs_rhb_outs = Column(Float)
    vs_rhb_so = Column(Integer)
    vs_rhb_er = Column(Integer)
    vs_rhb_h = Column(Integer)
    vs_rhb_bb = Column(Integer)
    vs_rhb_hr = Column(Integer)
    
    # Month stats
    month_outs = Column(Integer)
    month_so = Column(Integer)
    month_er = Column(Integer)
    month_h = Column(Integer)
    month_bb = Column(Integer)
    month_hr = Column(Integer)
    
    def __init__(self, pitcher):
        """ Constructor
        Copy the Pitcher object into the PitcherGameEntry fields
        :param pitcher: Pitcher object
        """
        self.first_name = pitcher.first_name
        self.last_name = pitcher.last_name
        self.pitch_fx_id = pitcher.pitch_fx_id
        self.game_id = pitcher.game_id
        self.team = pitcher.team
        self.draft_kings_points = pitcher.draft_kings_points
        self.game_date = pitcher.game_date
        
        # Game stats
        self.game_outs = pitcher.game_outs
        self.game_so = pitcher.game_so
        self.game_wins = pitcher.game_wins
        self.game_losses = pitcher.game_losses
        self.game_er = pitcher.game_er
        self.game_h = pitcher.game_h
        self.game_bb = pitcher.game_bb
        self.game_hr = pitcher.game_hr
        
        # Season stats
        self.season_outs = pitcher.season_outs
        self.season_so = pitcher.season_so
        self.season_wins = pitcher.season_wins
        self.season_losses = pitcher.season_losses
        self.season_er = pitcher.season_er
        self.season_h = pitcher.season_h
        self.season_bb = pitcher.season_bb
        self.season_hr = pitcher.season_hr
        
        # Career stats
        self.career_outs = pitcher.career_outs
        self.career_so = pitcher.career_so
        self.career_wins = pitcher.career_wins
        self.career_losses = pitcher.career_losses
        self.career_er = pitcher.career_er
        self.career_h = pitcher.career_h
        self.career_bb = pitcher.career_bb
        self.career_hr = pitcher.career_hr
        
        # Versus stats
        self.vs_outs = pitcher.vs_outs
        self.vs_so = pitcher.vs_so
        self.vs_er = pitcher.vs_er
        self.vs_h = pitcher.vs_h
        self.vs_bb = pitcher.vs_bb
        self.vs_hr = pitcher.vs_hr
        self.vs_lhb_outs = pitcher.vs_lhb_outs
        self.vs_lhb_so = pitcher.vs_lhb_so
        self.vs_lhb_er = pitcher.vs_lhb_er
        self.vs_lhb_h = pitcher.vs_lhb_h
        self.vs_lhb_bb = pitcher.vs_lhb_bb
        self.vs_lhb_hr = pitcher.vs_lhb_hr
        self.vs_rhb_outs = pitcher.vs_rhb_outs
        self.vs_rhb_so = pitcher.vs_rhb_so
        self.vs_rhb_er = pitcher.vs_rhb_er
        self.vs_rhb_h = pitcher.vs_rhb_h
        self.vs_rhb_bb = pitcher.vs_rhb_bb
        self.vs_rhb_hr = pitcher.vs_rhb_hr
        
        # Month stats
        self.month_outs = pitcher.month_outs
        self.month_so = pitcher.month_so
        self.month_er = pitcher.month_er
        self.month_h = pitcher.month_h
        self.month_bb = pitcher.month_bb
        self.month_hr = pitcher.month_hr
        
    def __repr__(self):
        """
        :return: string representation identifying the Pitcher entry
        """
        return "<User(name='%s %s')>" % (
                                self.first_name, self.last_name)




