from sqlalchemy import Column, String, ForeignKey
from mlb_database import Base


class LineupEntry(Base):
    """ Class for SQL entry of a chosen lineup

    The name of this SQL table is "lineup_entries."
    The primary key is a composition of the following member variables:
        game_date: the date of the chosen lineup in the following format (yyyy-mm-dd)
        game_time: the time at which the lineup was committed to the database
    The remaining variables represent the Rotowire IDs corresponding to each player
    """

    __tablename__ = 'lineup_entries'

    game_date = Column(String, primary_key=True)
    game_time = Column(String, primary_key=True)

    starting_pitcher_1 = Column(String, ForeignKey('pitcher_entries.rotowire_id'), primary_key=True)
    starting_pitcher_2 = Column(String, ForeignKey('pitcher_entries.rotowire_id'))
    catcher = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    first_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    second_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    third_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    shortstop = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    outfielder_1 = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    outfielder_2 = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    outfielder_3 = Column(String, ForeignKey('hitter_entries.rotowire_id'))