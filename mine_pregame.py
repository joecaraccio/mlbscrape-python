from mlbscrape_python.sql.mlb_database import MlbDatabase
from mlbscrape_python.mine.rotowire import RotoWire
from mlbscrape_python.mine.draft_kings import Draftkings
from datetime import date
from email_service import send_email

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

