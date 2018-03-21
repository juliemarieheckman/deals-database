import csv
from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
from datetime import date, timedelta
from os import remove
from site_configs import configs

END_DATE = '2020-01-01'
COPY_OFFER_FILE_NAME = '/Users/julie/Desktop/copy_file.sql'
OPEN_OFFERS_WHERE_CLAUSE = """
    WHERE
        source = '{deal_source}'
        and end_dt = '2020-01-01'
"""
ONE_DAY = timedelta(days=1)
CACHED_OFFER_FILE = '/Users/julie/Desktop/{deal_source}_offers.csv'

def build_where_clause(deal_source):
    return OPEN_OFFERS_WHERE_CLAUSE.format(deal_source = deal_source)

def get_database_connection():
    conn = connect("dbname='deals' user='julie' host='localhost'", cursor_factory=NamedTupleCursor)
    conn.autocommit = True
    cur = conn.cursor()
    return cur

def load_file_to_database(db_cxn):
    sql = "COPY deal_items FROM '{}';".format(COPY_OFFER_FILE_NAME)
    db_cxn.execute(sql)

def merge_new_to_open_offers(current_open, newly_found, offer_date, offer_source):

    merged_offer_set = []
    current_offers_transformed = [(c.item, c.value, c.details) for c in current_open]

    newly_found = list(newly_found)
    newly_found_transformed = [(n[1], n[2], n[3]) for n in newly_found]


    for offer in current_offers_transformed:
        current_offer = current_open[current_offers_transformed.index(offer)]
        if offer in newly_found_transformed:
            merged_offer_set.append((offer_source, str(current_offer.start_dt), END_DATE, current_offer.item, current_offer.value, current_offer.details))
            newly_found.pop(newly_found_transformed.index(offer))
            newly_found_transformed.remove(offer)
        else:
            merged_offer_set.append((offer_source, str(current_offer.start_dt), str(offer_date-ONE_DAY), current_offer.item, current_offer.value, current_offer.details))

    newly_found = [(offer_source, n[0], END_DATE, n[1], n[2], n[3]) for n in newly_found]
    merged_offer_set.extend(newly_found)

    return merged_offer_set

def drop_current_open_offers(db_cxn, deal_source):
    where_clause = build_where_clause(deal_source)
    sql = """
        DELETE
        
        FROM
            deal_items
        {}
    """.format(where_clause)
    db_cxn.execute(sql)

def build_copy_file(list_of_offers):
    sql_file = open(COPY_OFFER_FILE_NAME,'w')
    for o in list_of_offers:
        sql_file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(o[0],o[1],o[2],o[3].replace("'", "/'"),o[4],o[5]))

    sql_file.close()


def query_for_open_offers(db_cxn, deal_source):
    where_clause = build_where_clause(deal_source)
    sql = """ 
        SELECT
            start_dt,
            end_dt,
            replace(item, '/', '') as item,
            replace(value, '/', '') as value,
            replace(details, '/', '') as details
        from
            deal_items
        {}
    """.format(where_clause)
    db_cxn.execute(sql)
    rows = []
    if db_cxn.rowcount > 0:
        rows = db_cxn.fetchall()

    return rows

def load_deal_data(deal_source, db_cxn):

    deal_object = configs[deal_source]()

    deal_object.cache_deals_from_source()

    current_open_offers = query_for_open_offers(db_cxn, deal_source)

    cached_file = CACHED_OFFER_FILE.format(deal_source=deal_source)

    offers = csv.reader(open(cached_file), delimiter='|')

    merged_offers = merge_new_to_open_offers(current_open_offers, offers, date.today(), deal_source)

    build_copy_file(merged_offers)

    drop_current_open_offers(db_cxn, deal_source)

    load_file_to_database(db_cxn)

    remove(cached_file)

    remove(COPY_OFFER_FILE_NAME)

def do_all():
    db_cxn = get_database_connection()
    for deal_source in configs:
        load_deal_data(deal_source, db_cxn)

def do_specific(deal_site):
    db_cxn = get_database_connection()
    load_deal_data(deal_site, db_cxn)


# do_specific('coupons.com')
do_specific('cartwheel')
# do_all()
