

from sql.mlb_database import MlbDatabase
from mine.rotowire import mine_game_times
from sql.game import GameEntry
from datetime import date, datetime, timedelta
import time
from sqlalchemy import desc, asc
import sched
from mine.rotowire import mine_pregame_stats
from mine.draft_kings import Draftkings
from email_service import send_email

database_session = MlbDatabase().open_session()

# Mine the games
mine_game_times(database_session)
game_entries = database_session.query(GameEntry).filter(GameEntry.game_date == date.today())

# Group games by game times that are within 1 hour of one another
game_entries = list(game_entries.order_by(asc(GameEntry.game_time)))
game_groups = list()
game_group = list()
group_time = datetime.strptime(game_entries[0].game_date + " " + game_entries[0].game_time, "%Y-%m-%d %H:%M")
for game_entry in game_entries:
    game_time = datetime.strptime(game_entry.game_date + " " + game_entry.game_time, "%Y-%m-%d %H:%M")
    if game_time > group_time + timedelta(hours=1):
        game_groups.append(game_group)
        game_group = list()
        game_group.append(game_entry)
        group_time = game_time
    else:
        game_group.append(game_entry)
if len(game_group) > 0:
    game_groups.append(game_group)


def predict_contest(cutoff_time):
    #try:
    #TODO: get the Draftkings CSV first
    #database_session = MlbDatabase().open_session()
    mine_pregame_stats(cutoff_time)
    Draftkings.save_daily_csv()
    csv_dict = Draftkings.get_csv_dict()
    Draftkings.update_salaries(database_session, csv_dict)
    Draftkings.predict_daily_points(database_session, cutoff_time)
    optimal_lineup = Draftkings.get_optimal_lineup(database_session, cutoff_time)
    print optimal_lineup
    send_email(optimal_lineup.__str__())
    """except Exception as e:
        print e
        send_email("The predictor generated an exception: {0}".format(e))
    """

# Schedule the mining
#TODO: schedule immediately if we're inside the hour mark
game_scheduler = sched.scheduler(time.time, time.sleep)
for game_group in game_groups:
    group_time = datetime.strptime(game_group[0].game_date + " " + game_group[0].game_time, "%Y-%m-%d %H:%M") - timedelta(hours=1)
    group_time = datetime.strptime("2016-08-27 21:17", "%Y-%m-%d %H:%M")
    if datetime.now() < group_time:
        cutoff_time = datetime.strptime(game_group[len(game_group)-1].game_date + " " + game_entries[len(game_group)-1].game_time, "%Y-%m-%d %H:%M")
        game_scheduler.enterabs(time.mktime(group_time.timetuple()), priority=1, action=predict_contest,
                                argument=[cutoff_time])
        break

print game_scheduler.queue
game_scheduler.run()

database_session.close()