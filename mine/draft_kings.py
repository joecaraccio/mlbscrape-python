
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urlparse import urljoin
from urllib import urlretrieve
import time

# Class to interact with Draftkings and obtain the available players and salaries
class Draftkings(object):

    ROTOWIRE_DAILY_LINEUPS_URL = "http://www.rotowire.com/baseball/daily_lineups.htm"
    ROTOWIRE_LINK_TEXT = "See daily player values on DraftKings"
    
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


Draftkings.save_daily_csv()



