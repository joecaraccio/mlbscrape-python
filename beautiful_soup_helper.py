
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
        try:
            xml = urllib.urlopen(url)
        except IOError:
            print "Socket error."
            return None
        if xml.code == 404:
            print "Attempt to access invalid URL: " + xml.url
            raise Http404Exception(url)
        return BeautifulSoup(xml)

    @staticmethod
    def get_soup_from_url(url):
        try:
            for i in range(5):
                soup = BeautifulSoupHelper.url_to_soup(url)
                if soup is not None:
                    return soup
                else:
                    print "Trying to obtain soup again..."
        except Http404Exception:
            return None

        print "Exhausted all attempts to get the soup. Check your internet connection."
        return None

