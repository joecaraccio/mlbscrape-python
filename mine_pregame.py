import os
os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/mlbscrape_python")
from mlbscrape_python.sql.mlb_database import MlbDatabase
from mlbscrape_python.mine.rotowire import RotoWire
from mlbscrape_python.mine.draft_kings import Draftkings
from datetime import date, timedelta


mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

RotoWire.mine_pregame_stats(databaseSession)
Draftkings.save_daily_csv()
csv_dict = Draftkings.get_csv_dict()
Draftkings.update_salaries(databaseSession, csv_dict)
Draftkings.predict_daily_points(databaseSession, date.today())
tester = Draftkings.get_optimal_lineup(databaseSession, date.today())
print tester

databaseSession.close()

