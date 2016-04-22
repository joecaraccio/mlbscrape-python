
from mlb_database import Base
from sqlalchemy import Column, Integer, String, Float


class HitterGameEntry(Base):
    """ Class for SQL entry for a single game played by a hitter
    """
    __tablename__ = 'hitter_game_entries'
    
    pitch_fx_id = Column(String, primary_key=True)
    baseball_reference_id = Column(String, primary_key=True)
    game_id = Column(String, primary_key=True)
    draft_kings_points = Column(Float)
    first_name = Column(String)
    last_name = Column(String)
    team = Column(String)
    batting_order = Column(Integer)
    game_date = Column(String)
    
    # Game stats
    game_ab = Column(Integer)
    game_h = Column(Integer)
    game_bb = Column(Integer)
    game_so = Column(Integer)
    game_r = Column(Integer)
    game_sb = Column(Integer)
    game_cs = Column(Integer)
    game_hr = Column(Integer)
    game_rbi = Column(Integer)
    
    # Season stats
    season_ab = Column(Integer)
    season_h = Column(Integer)
    season_bb = Column(Integer)
    season_so = Column(Integer)
    season_r = Column(Integer)
    season_sb = Column(Integer)
    season_cs = Column(Integer)
    season_hr = Column(Integer)
    season_rbi = Column(Integer)
    
    # Career stats
    career_ab = Column(Integer)
    career_h = Column(Integer)
    career_bb = Column(Integer)
    career_so = Column(Integer)
    career_r = Column(Integer)
    career_sb = Column(Integer)
    career_cs = Column(Integer)
    career_hr = Column(Integer)
    career_rbi = Column(Integer)
    
    # Versus stats
    vs_ab = Column(Integer)
    vs_h = Column(Integer)
    vs_bb = Column(Integer)
    vs_so = Column(Integer)
    vs_hr = Column(Integer)
    vs_rbi = Column(Integer)
    vs_hand_ab = Column(Integer)
    vs_hand_h = Column(Integer)
    vs_hand_bb = Column(Integer)
    vs_hand_so = Column(Integer)
    vs_hand_r = Column(Integer)
    vs_hand_sb = Column(Integer)
    vs_hand_cs = Column(Integer)
    vs_hand_hr = Column(Integer)
    vs_hand_rbi = Column(Integer)
    
    # Month stats
    month_ab = Column(Integer)
    month_h = Column(Integer)
    month_bb = Column(Integer)
    month_so = Column(Integer)
    month_r = Column(Integer)
    month_sb = Column(Integer)
    month_cs = Column(Integer)
    month_hr = Column(Integer)
    month_rbi = Column(Integer)
    
    def __init__(self, hitter):
        """ Constructor
        :param hitter: Hitter object to copy the fields from
        """
        self.first_name = hitter.first_name
        self.last_name = hitter.last_name
        self.pitch_fx_id = hitter.pitch_fx_id
        self.baseball_reference_id = hitter.baseball_reference_id
        self.game_id = hitter.game_id
        self.team = hitter.team
        self.draft_kings_points = hitter.draftkings_points
        self.batting_order = hitter.batting_order
        self.game_date = hitter.game_date
        
        # Game stats
        self.game_ab = hitter.game_ab
        self.game_h = hitter.game_h
        self.game_bb = hitter.game_bb
        self.game_so = hitter.game_so
        self.game_r = hitter.game_r
        self.game_sb = hitter.game_sb
        self.game_cs = hitter.game_cs
        self.game_hr = hitter.game_hr
        self.game_rbi = hitter.game_rbi
        
        # Season stats
        self.season_ab = hitter.season_ab
        self.season_h = hitter.season_h
        self.season_bb = hitter.season_bb
        self.season_so = hitter.season_so
        self.season_r = hitter.season_r
        self.season_sb = hitter.season_sb
        self.season_cs = hitter.season_cs
        self.season_hr = hitter.season_hr
        self.season_rbi = hitter.season_rbi
        
        # Career stats
        self.career_ab = hitter.career_ab
        self.career_h = hitter.career_h
        self.career_bb = hitter.career_bb
        self.career_so = hitter.career_so
        self.career_r = hitter.career_r
        self.career_sb = hitter.career_sb
        self.career_cs = hitter.career_cs
        self.career_hr = hitter.career_hr
        self.career_rbi = hitter.career_rbi
        
        # Versus stats
        self.vs_ab = hitter.vs_ab
        self.vs_h = hitter.vs_h
        self.vs_bb = hitter.vs_bb
        self.vs_so = hitter.vs_so
        self.vs_hr = hitter.vs_hr
        self.vs_rbi = hitter.vs_rbi
        self.vs_hand_ab = hitter.vs_hand_ab
        self.vs_hand_h = hitter.vs_hand_h
        self.vs_hand_bb = hitter.vs_hand_bb
        self.vs_hand_so = hitter.vs_hand_so
        self.vs_hand_r = hitter.vs_hand_r
        self.vs_hand_sb = hitter.vs_hand_sb
        self.vs_hand_cs = hitter.vs_hand_cs
        self.vs_hand_hr = hitter.vs_hand_hr
        self.vs_hand_rbi = hitter.vs_hand_rbi
        
        # Month stats
        self.month_ab = hitter.month_ab
        self.month_h = hitter.month_h
        self.month_bb = hitter.month_bb
        self.month_so = hitter.month_so
        self.month_r = hitter.month_r
        self.month_sb = hitter.month_sb
        self.month_cs = hitter.month_cs
        self.month_hr = hitter.month_hr
        self.month_rbi = hitter.month_rbi
        
    def __repr__(self):
        """
        :return: string representation identifying the Hitter entry
        """
        return "<Hitter Game Entry(name='%s %s')>" % (
                                self.first_name, self.last_name)

    def to_input_vector(self):
        """ Transfer the object into a vector of its numerical variables
        :return: a list representation of the members of this class except the output
         DraftKings points
        """
        # Get the attributes of this class
        class_attributes = vars(self).items()
        input_vector = list()
        for attr in class_attributes:
            try:
                if type(attr[1]) == int or type(attr[1]) == float:
                    if attr[0] != "draft_kings_points":
                        input_vector.append(attr[1])
            except IndexError:
                print "Input tuple not correctly formatted."
                return None
            
        return input_vector
        




