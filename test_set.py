#!/usr/bin/python3

from argparse import ArgumentParser
import json
import logging
import os
import sys
import time
import unittest
import uuid

from main import readJsonFile
from set import Set, Card

from unittest.mock import patch
from unittest.mock import MagicMock

g_logger = logging.getLogger(__name__)
DEFAULT_LOGFMT = '%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(funcName)s %(message)s'
DEFAULT_DATEFMT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=DEFAULT_LOGFMT, datefmt=DEFAULT_DATEFMT, level=logging.DEBUG)

class TestSet(unittest.TestCase):
    def setUp(self):
        pass

    def test_set(self):
        pass

    def test_make_card_attributes(self):
        set = Set(logger=g_logger)

        test_cases = [
            [ 0, [0, 0, 0, 0], '1 Solid   Red   Oval     '],
            [ 1, [0, 0, 0, 1], '1 Solid   Red   Diamond  '],
            [ 2, [0, 0, 0, 2], '1 Solid   Red   Squiggle '],
            [ 3, [0, 0, 1, 0], '1 Solid   Green Oval     '],
            [ 6, [0, 0, 2, 0], '1 Solid   Blue  Oval     '],
            [ 9, [0, 1, 0, 0], '1 Open    Red   Oval     '],
            [18, [0, 2, 0, 0], '1 Striped Red   Oval     '],
            [27, [1, 0, 0, 0], '2 Solid   Red   Oval     '],
            [54, [2, 0, 0, 0], '3 Solid   Red   Oval     '],
        ]

        for index, test_case in enumerate(test_cases):
            value = test_case[0]
            expected_output = test_case[1]
            expected_string = test_case[2]
            g_logger.info(f"() Test case {index}: {value} -> {expected_output} '{expected_string}'")

            actual_output = set.make_card_attributes(value)
            #g_logger.info(f"() {actual_output=}")

            self.assertEqual(expected_output, actual_output)

            card = Card(actual_output)
            for i in range(4):
                actual_attribute = card.get_attribute(i)
                self.assertEqual(expected_output[i], actual_attribute)

            actual_string = card.to_string()
            self.assertEqual(expected_string, actual_string)

if __name__ == "__main__":
    unittest.main()
