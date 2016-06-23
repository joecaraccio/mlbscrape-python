
from bs4 import BeautifulSoup
import urllib
from datetime import date


class Http404Exception(Exception):

    def __init__(self, invalid_url):
        super(Http404Exception, self).__init__("Attempt to access invalid URL %s." % invalid_url)


class BeautifulSoupHelper(object):

    @staticmethod
    def str_to_date(date_string):
        """ Convert a PitchFx date string to a Date object
        :param date_string: a PitchFx date string
        :return the Date object representing the string
        """
        date_members = date_string.split("/")
        date_object = date(int(date_members[0]), int(date_members[1]), int(date_members[2]))
        return date_object

    @staticmethod
    def url_to_soup(url):
        """ Take a URL and get the BeautifulSoup object
        :param url: the absolute URL string
        :return the BeautifulSoup object returned, return None if the object was not successfully created
        """
        xml = urllib.urlopen(url)

        if xml.code == 404:
            print "Attempt to access invalid URL: " + xml.url
            raise Http404Exception(url)

        return BeautifulSoup(xml, "lxml")

    @staticmethod
    def get_soup_from_url(url):
        for i in range(5):
            try:
                soup = BeautifulSoupHelper.url_to_soup(url)
            except IOError:
                print "Socket error. Trying to obtain soup again."
                continue
            except Http404Exception:
                return None

            return soup

        print "Exhausted all attempts to get the soup. Check your internet connection."
        assert 0

