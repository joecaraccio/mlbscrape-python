from mine.stat_miner import *
from datetime import date, timedelta, datetime
from email_service import send_email
import cProfile

try:
    prefetch_pregame_stats()
    send_email("Prefetch games completed.")
except Exception as e:
    print e
    send_email("The predictor generated an exception: {0}".format(e))