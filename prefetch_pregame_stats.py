from mine.stat_miner import *
from datetime import date, timedelta, datetime
from email_service import send_email
import cProfile
import traceback

#try:
prefetch_pregame_stats()
csv_dict = get_csv_dict("players-" + str(date.today()) + ".csv")
update_salaries(csv_dict)
predict_daily_points()
optimal_lineup = get_optimal_lineup()
#except Exception as e:
#    print e
#    send_email("The predictor generated an exception: {0}".format(e))