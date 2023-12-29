import sys
import os
import random
import logging

from permutations import find_permutations, find_set_permutations

g_logger = None

class Attribute():
    def __init__(self, name, values):
        self.name = name
        self.values = values

        # find the longest value
        self.max_len = -1
        for value in values:
            self.max_len = max(self.max_len, len(value))

    def to_string(self, index: int) -> str:
        #g_logger.debug(f"({index=}) ENTER")
        if index >= len(self.values):
            raise ValueError(f"Attribute::to_string({index=}) out of bounds for attribute {self.name}")
        return f"{self.values[index]:{self.max_len}}"

    def num_values(self) -> int:
        return len(self.values)

class Card():
    g_parent = None

    @staticmethod
    def set_parent(parent) -> None:
        Card.g_parent = parent

    def __init__(self, attributes):
        #g_logger.debug(f"({attributes=}) ENTER")
        self.attributes = attributes

    def get_attribute(self, index: int) -> int:
        #g_logger.debug(f"({index=}) ENTER {self.attributes=}")
        return self.attributes[index]

    def get_attribute_string(self, index: int) -> str:
        #g_logger.debug(f"({index=}) ENTER {self.attributes=}")
        g_attributes = Card.g_parent.attributes
        g_attribute = g_attributes[index]
        return g_attributes[index].to_string(self.attributes[index])

    def to_string(self) -> str:
        #g_logger.debug(f"() ENTER {self.attributes=}")
        ret_string = ''
        g_attributes = Card.g_parent.attributes
        for index in range(len(g_attributes)):
            ret_string += self.get_attribute_string(index) + ' '
            #g_logger.debug(f"({self.attributes=}) {index=} {attribute.name=} {ret_string=}")

        #g_logger.debug(f"({self.attributes=}) LEAVE {ret_string=}")
        return ret_string


class Set():
    def __init__(self, config={}, logger=None):
        global g_logger
        g_logger = logger if logger is not None else logging.getLogger(__name__)

        Card.set_parent(self)

        g_logger.debug(f"({config=}) ENTER")

        default_num_cards_in_set = 3
        default_num_cards = 81
        default_num_cards_on_board = 12
        default_attributes = [
            {'name': 'Number', 'values': ['1', '2', '3']},
            {'name': 'Fill', 'values': ['Solid', 'Open', 'Striped']},
            {'name': 'Color', 'values': ['Red', 'Green', 'Blue']},
            {'name': 'Shape', 'values': ['Oval', 'Diamond', 'Squiggle']}
        ]

        self.num_cards_in_set = config.get('num_cards_in_set', default_num_cards_in_set)
        self.num_cards = config.get('num_cards', default_num_cards)
        self.num_cards_on_board = config.get('num_cards_on_board', default_num_cards_on_board)
        attributes = config.get('attributes', default_attributes)

        self.attributes = []
        for attribute in attributes:
            self.attributes.append(Attribute(attribute['name'], attribute['values']))

        self.cards = []
        for index in range(self.num_cards):
            card_attributes = self.make_card_attributes(index)
            c = Card(card_attributes)
            self.cards.append(c)
            #g_logger.debug(f"card[{index:4}] = {c.to_string()}")

    def make_card_attributes(self, value: int) -> [int]:
        #g_logger.debug(f"({value=}) ENTER")

        x = value # so that we have the original value for debug messages

        card_attributes = []

        for index, attribute in enumerate(self.attributes):
            # How many different values for this attribute?
            num_attribute_values = attribute.num_values()
            temp = x % num_attribute_values
            card_attributes.insert(0, temp)
            x = int(x / num_attribute_values)

        #g_logger.debug(f"({value=}) LEAVE {card_attributes=}")
        return card_attributes

    # Find out how many sets can be made from the cards on the board
    def find_num_sets(self) -> int:
        num_sets = 0

        for permutation in find_set_permutations(self.board, self.num_cards_in_set):
            if self.is_set(permutation):
                num_sets += 1

        return num_sets

    def find_a_set(self) -> [int]:
        num_cards_on_board = len(self.board)

        # TBD: If there are less than num_cards_in_set cards, bail
        if num_cards_on_board < self.num_cards_in_set:
            return None

        # Just for fun, how many sets are there?
        num_sets = self.find_num_sets()
        g_logger.info(f"() There are {num_sets} sets that can be made from the cards on the board")
        if num_sets == 0:
            return None

        # TBD: let the player hunt for the set(s)

        # Find the first set
        for permutation in find_permutations(len(self.board), self.num_cards_in_set):
            some_cards = [self.board[permutation[i]] for i in range(self.num_cards_in_set)]
            g_logger.debug(f"() checking {permutation=}\n     {some_cards}")
            if self.is_set(some_cards):
                return permutation

    def get_card(self) -> Card:
        return self.cards.pop(random.randrange(len(self.cards)))

    def add_card_to_board(self) -> Card:
        card = self.get_card()
        g_logger.debug(f"() '{card.to_string()}'")
        self.board.append(card)
        return card

    def add_cards_to_board(self, num_cards_to_add) -> None:
        num_cards_to_add = min(num_cards_to_add, len(self.cards))
        card_string = ''
        for i in range(num_cards_to_add):
            card = self.add_card_to_board()
            card_string += f"\n      {card.to_string()}"
        g_logger.debug(f"({num_cards_to_add=}){card_string}")

    def play(self):
        self.board = []
        self.add_cards_to_board(self.num_cards_on_board)

        while True:
            # print the board
            card_string = ''
            for index, card in enumerate(self.board):
                card_string += f"\n{index:4}: {card.to_string()} "
            g_logger.info(f"() Board:{card_string}")

            card_indexes = self.find_a_set()
            if card_indexes is None:
                g_logger.info(f"() didn't find a set! swapping cards")

                num_cards_to_swap = min(self.num_cards_in_set, len(self.cards))
                # If there are no more cards to swap, bail!
                if num_cards_to_swap == 0:
                    g_logger.info(f"() no more cards")
                    break

                # Take the first num_cards_to_swap off the board and put them in a temp pile
                temp = []
                for i in range(num_cards_to_swap):
                    temp.append(self.board.pop(0))
                # Take num_cards_to_swap from self.cards and put them on the board
                self.add_cards_to_board(num_cards_to_swap)
                # Take the cards from the temp pile and put them back into self.cards
                for i in range(num_cards_to_swap):
                    self.cards.append(temp.pop(0))

            else:
                card_string = ''
                for i in range(len(card_indexes)):
                    card = self.board[card_indexes[i]]
                    card_string += f"\n      {card.to_string()}"
                g_logger.info(f"() SET! {card_indexes=}{card_string}")

                # remove the cards from the board (in reverse order because of the ".pop()"
                for i in range(len(card_indexes), 0, -1):
                    self.board.pop(card_indexes[i-1])

                self.add_cards_to_board(self.num_cards_in_set)


    # return True if attribute[index] is the same for all of the cards
    def all_same(self, cards: [Card], index: int) -> bool:
        #g_logger.debug(f"({index=}) ENTER")

        status = True

        first_card = cards[0]
        for card_index in range(1, len(cards)):
            other_card = cards[card_index]
            g_logger.debug(f"({index=}) comparing:" \
                f"\n    first_card={first_card.to_string()}[{index}]='{first_card.get_attribute_string(index)}'" \
                f"\n    other_card={other_card.to_string()}[{index}]='{other_card.get_attribute_string(index)}'")

            if first_card.get_attribute(index) != other_card.get_attribute(index):
                status = False
                break

        g_logger.debug(f"({index=}) LEAVE {status=}")
        return status

    # return True if attribute[index] is different for all of the cards
    def all_different(self, cards: [Card], index: int) -> bool:
        #g_logger.debug(f"({index=}) ENTER")

        status = True
        # we have to exhaust all the permutations of cards (e.g, 1v2, 1v3, 2v3, ...)
        for card1_index in range(0, len(cards)-1):
            for card2_index in range(card1_index+1, len(cards)):
                card1 = cards[card1_index]
                card2 = cards[card2_index]

                if card1.get_attribute(index) == card2.get_attribute(index):
                    status = False
                    break

        g_logger.debug(f"({index=}) LEAVE {status=}")
        return status

    # return True if the cards match the "set" criteria
    def is_set(self, cards: [Card]) -> bool:
        card_string = ''
        for index, card in enumerate(cards):
            card_string += f"\n    card[{index}]={card.to_string()}"
        g_logger.debug(f"() ENTER{card_string}")

        status = True # assume the best

        all_same = 0
        all_different = 0
        mixed = 0
        for index in range(len(self.attributes)):
            if self.all_same(cards, index):
                all_same += 1
            elif self.all_different(cards, index):
                all_different += 1
            else:
                status = False
                mixed += 1

        if status:
            g_logger.debug(f"() Yes! This is a set! {all_same=} {all_different=}")

        g_logger.debug(f"() LEAVE {status=}{card_string}")
        return status

