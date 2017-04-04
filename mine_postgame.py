
from sql.mlb_database import MlbDatabase
from email_service import send_email
from mine.stat_miner import LineupMiner

try:
    mlbDatabase = MlbDatabase()
    lineup_miner = LineupMiner(lineup=None, opposing_pitcher=None, game_date=None, game_time=None,
                               db_path=None, is_home=False)
    lineup_miner.mine_yesterdays_results()
    send_email("Mine postgame completed.")
except Exception as e:
    print e
    send_email("The predictor generated an exception: {0}".format(e))