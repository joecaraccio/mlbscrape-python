
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from mlb_database import Base


class LineupHistoryEntry(Base):
    """ Class for SQL entry of yesterday's lineup for the given team
    """
    __tablename__ = 'lineup_history_entries'

    year = Column(Integer, primary_key=True)
    team = Column(String, primary_key=True)

    catcher = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    catcher_entry = relationship('HitterEntry', foreign_keys='HitterEntry.rotowire_id')
    first_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    second_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    third_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    shortstop = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    left_fielder = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    center_fielder = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    right_fielder = Column(String, ForeignKey('hitter_entries.rotowire_id'))