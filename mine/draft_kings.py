
from beautiful_soup_helper import BeautifulSoupHelper

# Class to interact with Draftkings and obtain the available players and salaries
class Draftkings(object):
    
    base_url = "https://www.draftkings.com/lobby#/MLB/0/All"
    
    def __init__(self):
        self.
        return
    
    @staticmethod
    def get_daily_csv(draftkings_link):
        draftkings_soup = BeautifulSoupHelper.get_soup_from_url(draftkings_link)

