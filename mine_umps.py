
from sql.mlb_database import MlbDatabase
from mine.stat_miner import UmpireMiner

game_miner = UmpireMiner('/home/cameron/mlb_stats.db')
game_miner.get_umpire_data()