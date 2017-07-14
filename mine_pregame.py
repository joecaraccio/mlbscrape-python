import os
from mine.draft_kings import save_daily_csv, get_csv_dict
from mine.stat_miner import predict_daily_points, get_optimal_lineup, mine_pregame_stats, update_salaries
from datetime import date, timedelta, datetime
import cProfile

try:
    mine_pregame_stats()
    # TODO: this is broken with Draftkings new structure
    #save_daily_csv()
    csv_dict = get_csv_dict("players-" + str(date.today()) + ".csv")
    update_salaries(csv_dict)
    predict_daily_points()
    optimal_lineup = get_optimal_lineup()
except Exception as e:
    print e
    print("The predictor generated an exception: {0}".format(e))
