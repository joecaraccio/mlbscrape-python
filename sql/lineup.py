from sqlalchemy import Column, String
from mlb_database import Base


class LineupEntry(Base):
    """ Class for SQL entry of a chosen lineup
    """

    __tablename__ = 'lineup_entries'

    game_date = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)

    starting_pitcher_1 = Column(String)
    starting_pitcher_2 = Column(String)
    catcher = Column(String)
    first_baseman = Column(String)
    second_baseman = Column(String)
    third_baseman = Column(String)
    shortstop = Column(String)
    outfielder_1 = Column(String)
    outfielder_2 = Column(String)
    outfielder_3 = Column(String)
