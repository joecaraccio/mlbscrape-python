import os
from sql.mlb_database import MlbDatabase
from mine.draft_kings import save_daily_csv, get_csv_dict
from mine.stat_miner import *
from datetime import date, timedelta, datetime
from email_service import send_email
import cProfile

os.chdir("/home/cameron/workspaces/MlbDatabase/mlb_scrape/Released/mlbscrape_python")

try:
    prefetch_pregame_stats()
except Exception as e:
    print e
    send_email("The predictor generated an exception: {0}".format(e))