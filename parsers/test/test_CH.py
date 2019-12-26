#!/usr/bin/env python3

"""Tests for CH.py"""

import json
import unittest
from arrow import get
from datetime import datetime
from parsers import CH
from unittest.mock import patch


class ExchangeTestcase(unittest.TestCase):
    """
    Tests for fetch_exchange.
    Patches in a fake response from the data source to allow repeatable testing.
    """

    def setUp(self):
        with open('parsers/test/mocks/CH.json') as f:
            self.fake_data = json.load(f)

        with patch('parsers.CH.get_data', return_value = self.fake_data) as gd:
            self.data = CH.fetch_exchange('CH', 'FR')


    def test_is_not_none(self):
        data = self.data
        self.assertIsNotNone(data)

    def test_key_match(self):
        data = self.data
        self.assertEqual(data['sortedZoneKeys'], 'CH->FR')


    def test_flow_importing(self):
        data = self.data
        self.assertEqual(data['netFlow'], -2234.0)

    def test_flow_exporting(self):
        with patch('parsers.CH.get_data', return_value = self.fake_data) as gd:
            self.data = CH.fetch_exchange('CH', 'FR')
            data = CH.fetch_exchange('CH', 'IT-NO')
            self.assertEqual(data['netFlow'], 1304.0)


    def test_source(self):
        data = self.data
        self.assertEqual(data['source'], 'swissgrid.ch')

if __name__ == '__main__':
    unittest.main()
