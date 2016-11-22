

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

# Base instance for managing all the objects
Base = declarative_base()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class MlbDatabase(object):
    """ Class for managing SQL databases
    """

    def __init__(self, path=None):
        """ Constructor
        Create/open a local database.
        """
        # Import all the metadata
        from sql.game import GameEntry
        from sql.hitter_entry import HitterEntry
        from sql.pitcher_entry import PitcherEntry
        from sql.pregame_hitter import PregameHitterGameEntry
        from sql.pregame_pitcher import PregamePitcherGameEntry
        from sql.postgame_hitter import PostgameHitterGameEntry
        from sql.postgame_pitcher import PostgamePitcherGameEntry
        from sql.lineup import LineupEntry

        if path is None:
            path = 'sqlite:////mlb_stats.db'
        else:
            path = 'sqlite:///' + path

        # Create/open a local database
        engine = create_engine(path, echo=False)
        Base.metadata.create_all(engine)
        self.sessionMaker = sessionmaker(bind=engine)

    def open_session(self):
        """ Open a session of the database
        :return: a Session instance
        """
        return self.sessionMaker()