import os
from sql.mlb_database import MlbDatabase
from mine.rotowire import mine_pregame_stats
from mine.draft_kings import Draftkings
from datetime import date, timedelta
from email_service import send_email
import cProfile

os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/Released/mlbscrape_python")

databaseSession = MlbDatabase().open_session()

#try:
    #cProfile.run('mine_pregame_stats()')
    #Draftkings.save_daily_csv()
    #csv_dict = Draftkings.get_csv_dict()
    #Draftkings.update_salaries(databaseSession, csv_dict)
Draftkings.predict_daily_points(databaseSession, date.today())
optimal_lineup = Draftkings.get_optimal_lineup(databaseSession, date.today())
print optimal_lineup
send_email(optimal_lineup.__str__())
"""except Exception as e:
    print e
    send_email("The predictor generated an exception: {0}".format(e))
"""
databaseSession.close()

