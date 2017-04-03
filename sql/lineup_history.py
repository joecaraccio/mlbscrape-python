
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
    catcher_entry = relationship('HitterEntry', foreign_keys=[catcher])
    first_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    first_baseman_entry = relationship('HitterEntry', foreign_keys=[first_baseman])
    second_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    second_baseman_entry = relationship('HitterEntry', foreign_keys=[second_baseman])
    third_baseman = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    third_baseman_entry = relationship('HitterEntry', foreign_keys=[third_baseman])
    shortstop = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    shortstop_entry = relationship('HitterEntry', foreign_keys=[shortstop])
    left_fielder = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    left_fielder_entry = relationship('HitterEntry', foreign_keys=[left_fielder])
    center_fielder = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    center_fielder_entry = relationship('HitterEntry', foreign_keys=[center_fielder])
    right_fielder = Column(String, ForeignKey('hitter_entries.rotowire_id'))
    right_fielder_entry = relationship('HitterEntry', foreign_keys=[right_fielder])