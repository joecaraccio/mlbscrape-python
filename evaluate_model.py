

from sql.mlb_database import MlbDatabase
from sql.lineup import LineupEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.pregame_hitter import PregameHitterGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from datetime import date, timedelta
from numpy import array, std, mean

database_session = MlbDatabase().open_session()

query_results = database_session.query(LineupEntry).filter(LineupEntry.game_date != date.today())
lineup_predicted_salary = 0
lineup_actual_salary = 0
lineup_actual_vector = list()
lineup_predicted_vector = list()
for query_result in query_results:
    try:
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.catcher, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgamePitcherGameEntry).get((query_result.starting_pitcher_1, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgamePitcherGameEntry).get((query_result.starting_pitcher_2, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.first_baseman, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.second_baseman, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.third_baseman, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.shortstop, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.outfielder_1, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.outfielder_2, query_result.game_date)).actual_draftkings_points
        lineup_actual_salary += database_session.query(PostgameHitterGameEntry).get((query_result.outfielder_3, query_result.game_date)).actual_draftkings_points

        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.catcher, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregamePitcherGameEntry).get((query_result.starting_pitcher_1, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregamePitcherGameEntry).get((query_result.starting_pitcher_2, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.first_baseman, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.second_baseman, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.third_baseman, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.shortstop, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.outfielder_1, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.outfielder_2, query_result.game_date)).predicted_draftkings_points
        lineup_predicted_salary += database_session.query(PregameHitterGameEntry).get((query_result.outfielder_3, query_result.game_date)).predicted_draftkings_points

        print lineup_actual_salary, lineup_predicted_salary
        lineup_predicted_vector.append(lineup_predicted_salary)
        lineup_actual_vector.append(lineup_actual_salary)
    except AttributeError:
        print "No postgame data found for a player in this lineup."
    finally:
        lineup_predicted_salary = 0
        lineup_actual_salary = 0

lineup_predicted_vector = array(lineup_predicted_vector)
lineup_actual_vector = array(lineup_actual_vector)
print "Mean: %f, Std. dev: %f" % (mean(lineup_predicted_vector-lineup_actual_vector),
                                  std(lineup_predicted_vector-lineup_actual_vector))

database_session.close()