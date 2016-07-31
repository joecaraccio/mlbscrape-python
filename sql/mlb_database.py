

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base instance for managing all the objects
Base = declarative_base()


class MlbDatabase(object):
    """ Class for managing SQL databases
    """

    def __init__(self):
        """ Constructor
        Create/open a local database.
        """
        # Create/open a local database
        engine = create_engine('sqlite:////home/cameron/workspaces/MlbDatabase/mlb_scrape/Released/mlbscrape_python/mlb_stats.db', echo=False)
        Base.metadata.create_all(engine)
        self.sessionMaker = sessionmaker(bind=engine)

    def open_session(self):
        """ Open a session of the database
        :return: a Session instance
        """
        return self.sessionMaker()

mlb_database = MlbDatabase()