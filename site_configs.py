
from collect_web_info_from_cards import CardStyleDealsPage
from collect_web_info_from_page import DealsPage

class Ibotta(CardStyleDealsPage):

    def __init__(self):
        CardStyleDealsPage.__init__(self)
        self.url = "https://ibotta.com/rebates?retailer=target"
        self.data_section = 'offer-card-content'
        self.offer_section = 'offer-grid'
        self.deal_source = 'ibotta'


    def _parse_offer_row(self, offer_row):

        deal = self._strip_non_ascii(offer_row[1])
        item = self._strip_non_ascii(offer_row[0])
        store = self._strip_non_ascii(offer_row[2])
        return_dict = dict(
            deal=deal,
            item=item,
            details=store
        )
        #
        # return  return_dict

        return return_dict


class Cartwheel(CardStyleDealsPage):

    def __init__(self):
        CardStyleDealsPage.__init__(self)
        self.url = "https://cartwheel.target.com/browseall"
        self.data_section = 'offer-card-data'
        self.offer_section = 'ng-scope'
        self.deal_source = 'cartwheel'
        self.scroll_pause_time = 10
        self.scroll_count = 25

    def _parse_offer_row(self, offer_row):

        deal = self._strip_non_ascii(offer_row[0])
        item = self._strip_non_ascii(offer_row[-1])

        detail_values = [self._strip_non_ascii(o) for o in offer_row[1:-1]]
        details = ', '.join(detail_values)

        return_dict = dict(
            deal=deal,
            item=item,
            details=details
        )

        return return_dict


class CouponsCom(CardStyleDealsPage):
    def __init__(self):
        CardStyleDealsPage.__init__(self)
        self.url = "https://www.coupons.com/"
        self.data_section = 'wrapper'
        self.offer_section = 'mod-gallery'
        self.deal_source = 'coupons.com'
        self.scroll_pause_time = 1
        self.scroll_count = 1

    def _parse_offer_row(self, offer_row):

        print(offer_row)
        deal = self._strip_non_ascii(offer_row[0])
        item = self._strip_non_ascii(offer_row[-1])

        detail_values = [self._strip_non_ascii(o) for o in offer_row[1:-1]]
        details = ', '.join(detail_values)

        return_dict = dict(
            deal=deal,
            item=item,
            details=details
        )

        return return_dict


#ToDo RedPlum Coupons
#ToDo Coupons.com (pod-info (summary, brand, details)), mod-gallery

configs = {
    'ibotta': Ibotta,
    'cartwheel': Cartwheel
}