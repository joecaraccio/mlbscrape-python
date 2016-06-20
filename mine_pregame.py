import os
from sql.mlb_database import MlbDatabase
from mine.rotowire import RotoWire
from mine.draft_kings import Draftkings
from datetime import date, timedelta
from email_service import send_email

os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/Released/mlbscrape_python")

mlbDatabase = MlbDatabase()
databaseSession = mlbDatabase.open_session()

RotoWire.mine_pregame_stats(databaseSession)
Draftkings.save_daily_csv()
csv_dict = Draftkings.get_csv_dict()
Draftkings.update_salaries(databaseSession, csv_dict)
Draftkings.predict_daily_points(databaseSession, date.today())
optimal_lineup = Draftkings.get_optimal_lineup(databaseSession, date.today())
print optimal_lineup
send_email(optimal_lineup.__str__())

databaseSession.close()

