from selenium import webdriver
import time
from datetime import date

SCROLL_COUNT = 10
SCROLL_PAUSE_TIME = 1.0

class CardStyleDealsPage(object):

    def __init__(self):
        self.driver = None
        self.deal_source = None
        self.url = None
        self.data_section = None
        self.offer_section = None
        self.scroll_count = SCROLL_COUNT
        self.scroll_pause_time = SCROLL_PAUSE_TIME

    def _strip_non_ascii(self, string):
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def _get_web_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(60)
        self.driver.maximize_window()

    def _collect_offer_cards(self):
        self.driver.get(self.url)

        time.sleep(self.scroll_pause_time)
        scrollCount = 1
        last_height = 0
        scroll_count_same = 0
        offers = open('/Users/julie/Desktop/{}_offers.csv'.format(self.deal_source), 'a')

        while True:

            self.driver.execute_script("window.scrollTo(0, " + str(scrollCount * 500) + ");")

            time.sleep(self.scroll_pause_time)
            scrollCount += 1

            e = self.driver.find_element_by_class_name(self.offer_section)
            size = e.size

            h = size['height']

            if h == last_height:
                scroll_count_same += 1
            else:
                scroll_count_same = 0

            if scroll_count_same > self.scroll_count:
                break

            last_height = h

        element = self.driver.find_element_by_class_name(self.offer_section)
        offer_cards = element.find_elements_by_class_name(self.data_section)

        data = offer_cards.text.split('\n')
        parsed_data = self._parse_offer_row(data)
        print parsed_data
        offers.write('{}|{}|{}|{}\n'.format(date.today(), parsed_data['deal'], parsed_data['item'], parsed_data['details']))

    def _parse_offer_row(self, offer_row):
        raise NotImplementedError

    def cache_deals_from_source(self):
        self._get_web_driver()
        self._collect_offer_cards()
        self.driver.quit()




