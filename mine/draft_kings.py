
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urlparse import urljoin
from urllib import urlretrieve
import csv
import time
from datetime import date
from mlbscrape_python.sql.pregame_hitter import PregameHitterGameEntry
from mlbscrape_python.sql.pregame_pitcher import PregamePitcherGameEntry
from mlbscrape_python.sql.hitter_entry import HitterEntry
from mlbscrape_python.sql.pitcher_entry import PitcherEntry

# Class to interact with Draftkings and obtain the available players and salaries
class Draftkings(object):

    ROTOWIRE_DAILY_LINEUPS_URL = "http://www.rotowire.com/baseball/daily_lineups.htm"
    ROTOWIRE_LINK_TEXT = "See daily player values on DraftKings"

    class NameNotFound(Exception):
        def __init__(self, name):
            super(Draftkings.NameNotFound, self).__init__("Name '%s' not found in the Baseball Reference page" %
                                                                  name)

    @staticmethod
    def save_daily_csv():
        browser = webdriver.Firefox()
        browser.get(Draftkings.ROTOWIRE_DAILY_LINEUPS_URL)
        draftkings_button = browser.find_element_by_link_text(Draftkings.ROTOWIRE_LINK_TEXT)
        draftkings_button.click()
        browser.switch_to.window(browser.window_handles[len(browser.window_handles)-1])
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'fancybox-outer')))
        print("Page loaded")
        browser.find_element_by_id("fancybox-close").click()
        #wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "tabs")]/ul/li[text() = "All"]')))
        #browser.find_element_by_xpath('//div[contains(@class, "tabs")]/ul/li[text() = "All"]').click()

        # download the file
        csv_url = urljoin(browser.current_url, browser.find_element_by_css_selector("a.export-to-csv").get_attribute("href"))
        urlretrieve(csv_url, "players.csv")

    @staticmethod
    def get_csv_dict():
        """ Create a dictionary of dictionaries indexed by a concatentation of name and Draftkings team abbreviation
        """
        csv_dict = dict()
        with open('players.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print (row["Name"] + row["teamAbbrev"]).lower()
                csv_dict[(row["Name"] + row["teamAbbrev"]).lower()] = row

        return csv_dict

    @staticmethod
    def update_salaries(database_session, csv_dict=None, game_date=None):
        if game_date is None:
            game_date = date.today()
        if csv_dict is None:
            csv_dict = Draftkings.get_csv_dict()
        #Hitters
        pregame_hitters = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == game_date)
        for pregame_entry in pregame_hitters:
            # Lookup the player's name in the database
            # Lookup the name in the dictionary
            hitter_entry = database_session.query(HitterEntry).filter(HitterEntry.rotowire_id == pregame_entry.rotowire_id)[0]
            try:
                csv_entry = csv_dict[(hitter_entry.first_name + " " + hitter_entry.last_name + hitter_entry.team).lower()]
                pregame_entry.draftkings_salary = int(csv_entry["Salary"])
                database_session.commit()
            except KeyError:
                print "Player %s not found in the Draftkings CSV file." % (hitter_entry.first_name + " " + hitter_entry.last_name)

        # Pitchers
        pregame_pitchers = database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == game_date)
        for pregame_entry in pregame_pitchers:
            # Lookup the player's name in the database
            # Lookup the name in the dictionary
            pitcher_entry = database_session.query(PitcherEntry).filter(PitcherEntry.rotowire_id == pregame_entry.rotowire_id)[0]
            try:
                csv_entry = csv_dict[(pitcher_entry.first_name + " " + pitcher_entry.last_name + pitcher_entry.team).lower()]
                pregame_entry.draftkings_salary = int(csv_entry["Salary"])
                database_session.commit()
            except KeyError:
                print "Player %s not found in the Draftkings CSV file." % (pitcher_entry.first_name + " " + pitcher_entry.last_name)

    @staticmethod
    def get_hitter_points(postgame_hitter):
        points = float()
        points += 3*postgame_hitter.game_1b
        points += 5*postgame_hitter.game_2b
        points += 8*postgame_hitter.game_3b
        points += 10*postgame_hitter.game_hr
        points += 2*postgame_hitter.game_rbi
        points += 2*postgame_hitter.game_r
        points += 2*postgame_hitter.game_bb
        points += 2*postgame_hitter.game_hbp
        points += 5*postgame_hitter.game_sb

        return points

    @staticmethod
    def get_pitcher_points(postgame_pitcher):
        points = float()
        string_ip = str(postgame_pitcher.game_ip)
        innings_pitched_float = 0.333*float(string_ip.split(".")[1]) + float(string_ip.split(".")[0])
        points += 2.25*innings_pitched_float
        points += 2*postgame_pitcher.game_so
        points += 4*postgame_pitcher.game_wins
        points -= 2*postgame_pitcher.game_er
        points -= 0.6*postgame_pitcher.game_h
        points -= 0.6*postgame_pitcher.game_bb
        points -= 0.6*postgame_pitcher.game_hbp
        points += 2.5*postgame_pitcher.game_cg
        points += 2.5*postgame_pitcher.game_cgso
        points += 5*postgame_pitcher.game_no_hitter

        return points