from selenium import webdriver
from datetime import date

SCROLL_COUNT = 10
SCROLL_PAUSE_TIME = 1.0

class DealsPage(object):

    def __init__(self):

        self.driver = None
        self.deal_source = None
        self.url = None
        self.data_section = None
        self.offer_section = None

    def _strip_non_ascii(self, string):
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def _get_web_driver(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.driver.maximize_window()

    def _collect_offer_cards(self):

        self.driver.get(self.url)

        element = self.driver.find_element_by_class_name('offer')

        offer_cards = element.find_elements_by_class_name('normal')

        return offer_cards

    def _write_offer_file(self, offer_cards):

        offers = open('/Users/julie/Desktop/{}_offers.csv'.format(self.deal_source), 'a')

        for o in offer_cards:

            data = o.text.split('\n')
            parsed_data = self._parse_offer_row(data)
            offers.write('{},{},{},{}\n'.format(date.today(), parsed_data['deal'], parsed_data['item'], parsed_data['details']))

        offers.close()

    def _parse_offer_row(self, offer_row):
        raise NotImplementedError

    def cache_deals_from_source(self):

        self._get_web_driver()
        cards = self._collect_offer_cards()
        self._write_offer_file(cards)
        self.driver.quit()