import os
from mine.draft_kings import save_daily_csv, get_csv_dict
from mine.stat_miner import predict_daily_points, get_optimal_lineup, mine_pregame_stats, update_salaries
from datetime import date, timedelta, datetime
from email_service import send_email
import cProfile

try:
    mine_pregame_stats()
    save_daily_csv()
    csv_dict = get_csv_dict()
    update_salaries(csv_dict)
    predict_daily_points(date.today())
    optimal_lineup = get_optimal_lineup(date.today())
    print optimal_lineup
    send_email(optimal_lineup.__str__())
except Exception as e:
    print e
    send_email("The predictor generated an exception: {0}".format(e))