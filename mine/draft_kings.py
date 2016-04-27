
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urlparse import urljoin
from urllib import urlretrieve
import csv
import time

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
        #browser.find_element_by_xpath('//div[contains(@class, "tabs")]/ul/li[text() = "All"]').click()

        # download the file
        csv_url = urljoin(browser.current_url, browser.find_element_by_css_selector("a.export-to-csv").get_attribute("href"))
        urlretrieve(csv_url, "players.csv")

    @staticmethod
    def get_csv_dict():
        csv_dict = dict()
        with open('players.csv') as csvfile:
            reader = csv.DictReader(csvfile)
        #TODO: we really want an ordered multiset here so we can have duplicate names but it is still ordered
        return csv_dict

"""
    @staticmethod
    def update_salaries(pregame_entries, csv_dict=None):
        if csv_dict is None:
            csv_dict = Draftkings.get_csv_dict()
        for pregame_entry in pregame_entries:
            # Lookup the player's name in the database
            # Lookup the name in the dictionary
            try:
                csv_entry = csv_dict[pregame_entry.
"""



