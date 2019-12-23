#!/usr/bin/python3
# -*- coding: utf-8 -*-

import arrow
import re
import dateutil
import requests
import json

EXCHANGE_URL = 'https://www.swissgrid.ch/bin/services/apicache?path=/content/swissgrid/fr/home/operation/grid-data/current-data/jcr:content/parsys/livedatawidget_copy'

# We use the arrow direction to determine if we are exporting or importing energy
ZONE_EXPORT_ARROW_DIRECTION = {
    'de': 'up',
    'it': 'down',
    'fr': 'left',
    'at': 'right'
}

def format_zone_keys(zone_key1, zone_key2, is_exporting):
    return zone_key1 + '->' + zone_key2 if is_exporting else zone_key2 + '->' + zone_key1

def is_exporting(zone_key, arrow_direction):
    return ZONE_EXPORT_ARROW_DIRECTION[zone_key] == arrow_direction

def parse_flow(flow_string):
    return float(flow_string.split(' ')[0])

def fetch_exchange(zone_key1, zone_key2, session=None, target_datetime=None, logger=None):
    """Requests the last known power exchange (in MW) between two zones
    Arguments:
    zone_key1           -- the first country code
    zone_key2           -- the second country code; order of the two codes in params doesn't matter
    session (optional)      -- request session passed in order to re-use an existing session
    target_datetime (optional) -- used if parser can fetch data for a specific day, str in format YYYYMMDD
    logger (optional) -- handles logging when parser is run as main
    Return:
    A list of dictionaries in the form:
    {
      'sortedZoneKeys': 'DK->NO',
      'datetime': '2017-01-01T00:00:00Z',
      'netFlow': 0.0,
      'source': 'mysource.com'
    }
    where net flow is from DK into NO
    """
    now = arrow.utcnow().format()

    r = session or requests.session()
    response = r.get(EXCHANGE_URL)
    data = json.loads(response.text)['data']['marker']
    result = map(lambda x: {
        'sortedZoneKeys': format_zone_keys('CH', x['id'].upper(), is_exporting(x['id'], x['direction'])),
        'datetime': now,
        'netFlow': parse_flow(x['text2']),
        'source': 'swissgrid.ch'
    }, data)
    return list(result)

if __name__ == '__main__':
    print('fetch_exchange(RU-1, RU-2) ->')
    print(fetch_exchange('RU-1', 'RU-2'))
