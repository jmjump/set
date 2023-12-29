#!/usr/bin/python3

from argparse import ArgumentParser
import json
import logging
import os
import sys
import time
import unittest
import uuid

from unittest.mock import patch
from unittest.mock import MagicMock

from permutations import find_permutations, find_set_permutations

g_logger = logging.getLogger(__name__)
DEFAULT_LOGFMT = '%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(funcName)s %(message)s'
DEFAULT_DATEFMT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=DEFAULT_LOGFMT, datefmt=DEFAULT_DATEFMT, level=logging.DEBUG)

def check_for_item_on_list(expected_item, actual_list):
    g_logger.debug(f"({expected_item=}, {actual_list=}) ENTER")
    for actual_item in actual_list:
        g_logger.debug(f"() checking {actual_item=}")
        if type(actual_item) is list:
            g_logger.debug(f"() checking {actual_item=}, which is a list")
            if order_insensitive_compare(expected_item, actual_item):
                g_logger.debug(f"() return False for {expected_item=} {actual_item=}")
                return True
        elif actual_item == expected_item:
            return True

    # If we made it this far, we good
    g_logger.debug(f"({expected_item=}, {actual_list=}) LEAVE return False")
    return False

def order_insensitive_compare(list1, list2):
    g_logger.debug(f"(\n{list1=}, \n{list2=}) ENTER")
    # Make sure the list have the same number of items
    if len(list1) != len(list2):
        return False

    # Make sure all the items from list1 one are in list2
    for list1_item in list1:
        g_logger.debug(f"() checking {list1_item=}")
        if not check_for_item_on_list(list1_item, list2):
            return False

    # Make sure all the items from list2 one are in list1
    for list2_item in list2:
        g_logger.debug(f"() checking {list2_item=}")
        if not check_for_item_on_list(list2_item, list1):
            return False

    # If we made if this far, we good
    g_logger.debug(f"(\n{list1=}, \n{list2=}) LEAVE return True")
    return True

class TestPermutations(unittest.TestCase):
    def test_find_permutations(self):
        actual_values = [permutation.copy() for permutation in find_permutations(6, 3)]

        expected_values = [
                [0, 1, 2],
                [0, 1, 3],
                [0, 1, 4],
                [0, 1, 5],
                [0, 2, 3],
                [0, 2, 4],
                [0, 2, 5],
                [0, 3, 4],
                [0, 3, 5],
                [0, 4, 5],

                [1, 2, 3],
                [1, 2, 4],
                [1, 2, 5],
                [1, 3, 4],
                [1, 3, 5],
                [1, 4, 5],

                [2, 3, 4],
                [2, 3, 5],
                [2, 4, 5],

                [3, 4, 5],
            ]

        self.assertTrue(order_insensitive_compare(expected_values, actual_values))

    def test_find_set_permutations(self):
        set = ['a', 'e', 'i', 'o', 'u']
        actual_values = [permutation.copy() for permutation in find_set_permutations(set, 2)]

        expected_values = [
                ['a', 'e'],
                ['a', 'i'],
                ['a', 'o'],
                ['a', 'u'],
                ['e', 'i'],
                ['e', 'o'],
                ['e', 'u'],
                ['i', 'o'],
                ['i', 'u'],
                ['o', 'u']
            ]

        self.assertTrue(order_insensitive_compare(expected_values, actual_values))

if __name__ == "__main__":
    unittest.main()

