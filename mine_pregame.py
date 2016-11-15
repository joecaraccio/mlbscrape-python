import os
from sql.mlb_database import MlbDatabase
from mine.rotowire import mine_pregame_stats
from mine.draft_kings import save_daily_csv, get_csv_dict, update_salaries, predict_daily_points, get_optimal_lineup
from datetime import date, timedelta, datetime
from email_service import send_email
import cProfile

os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/Released/mlbscrape_python")

databaseSession = MlbDatabase().open_session()

try:
    mine_pregame_stats()
    save_daily_csv()
    csv_dict = get_csv_dict()
    update_salaries(databaseSession, csv_dict)
    predict_daily_points(databaseSession, date.today())
    optimal_lineup = get_optimal_lineup(databaseSession, date.today())
    print optimal_lineup
    send_email(optimal_lineup.__str__())
except Exception as e:
    print e
    send_email("The predictor generated an exception: {0}".format(e))

databaseSession.close()

