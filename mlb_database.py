

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base instance for managing all the objects
Base = declarative_base()

class MlbDatabase(object):
    
    def __init__(self):
        # Create/open a local database
        engine = create_engine('sqlite:///mlb.db', echo=False)
        
        Base.metadata.create_all(engine)

        # Factory for new sessions
        self.sessionMaker = sessionmaker(bind=engine)
        
    
    def open_session(self):
        # New session with the database
        return self.sessionMaker()