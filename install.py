

import os
import sqlite3
import requests


def setup(db):
    db.execute("""
        CREATE TABLE legislators
        (first_name, last_name, title, party, chamber, birthday, 
            state, term_start, term_end);
    """)


def download():
    """
    {u'last_name': u'Babin', u'state_name': u'Texas', 
        u'office': u'316 Cannon House Office Building', 
        u'thomas_id': u'02270', u'first_name': 
        u'Brian', u'middle_name': None, u'district': 36, u'title': u'Rep', 
        u'in_office': True, u'state': u'TX', u'term_end': u'2017-01-03', 
        u'crp_id': u'N00005736', u'oc_email': u'Rep.Babin@opencongress.org', 
        u'party': u'R', u'fec_ids': [u'H6TX02079'], 
        u'website': u'http://babin.house.gov', u'fax': u'202-226-0396', 
        u'leadership_role': None, u'govtrack_id': u'412655', 
        u'facebook_id': u'RepBrianBabin', u'bioguide_id': u'B001291', 
        u'birthday': u'1948-03-23', u'term_start': u'2015-01-06', 
        u'nickname': None, u'contact_form': None, 
        u'ocd_id': u'ocd-division/country:us/state:tx/cd:36', 
        u'phone': u'202-225-1555', u'gender': u'M', u'name_suffix': None, 
        u'twitter_id': u'RepBrianBabin', u'chamber': u'house'
    }
    """
    res = requests.get(
        'https://congress.api.sunlightfoundation.com/legislators', headers={
            'X-APIKEY' : os.environ.get('SUNLIGHT_API_KEY'),
        }
    )

    return res.json()


def load(db, legislators):
    """
    INSERT INTO legislators 
        (first_name, last_name, party, chamber, state) 
    VALUES 
        ('Thom', 'Tillis', 'R', 'senate', 'NC');
    """

    fields = ['first_name', 'last_name', 'party', 'chamber', 'state']

    for legislator in legislators.get('results'):
        values = [ legislator.get(field) for field in fields ]
        sql = "INSERT INTO legislators ({fields}) VALUES ('{values}');".format(
            fields=', '.join(fields), values="', '".join(values))
        print sql
        db.execute(sql)


def main(db):
    legislators = download()
    setup(db)
    load(db, legislators)


if __name__ == '__main__':
    with sqlite3.connect('congress.db') as conn:
        cursor = conn.cursor()
        main(cursor)
