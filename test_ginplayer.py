from ginplayer import *
from ginhand import *
from gintable import *
import unittest


class TestGinPlayer(unittest.TestCase):
    def test_new_ginplayer(self):
        s = GinStrategy()
        p = GinPlayer(s)

        # the guid shouldn't be a predictable number (this will fail 1 in 2**128 times)
        self.assertNotEqual(123456, p.id)

        # has a GinStrategy
        self.assertIsInstance(p.strategy, GinStrategy, "Does not contain a GinStrategy")

        # has a GinHand
        self.assertIsInstance(p.hand, GinHand, "Does not contain a GinHand")

        # allows other classes to observe potential knocks
        self.assertIsInstance(p._knock_listeners, list, "Does not implement observer on knocks")

        # allows other classes to observe potential gin calls
        self.assertIsInstance(p._knock_gin_listeners, list, "Does not implement observer on gins")

    def test_sit_at_table(self):
        p = GinPlayer()
        t = GinTable()

        # sit down and ensure table is made of wood
        p.sit_at_table(t)
        self.assertIsInstance(p.table, GinTable, "Player not sitting at GinTable")

    def test__add_card(self):
        p = GinPlayer()

        # verify empty hand
        self.assertEqual(p.hand.size(), 0)

        # draw a card and verify length of hand is 1
        p._add_card(GinCard(9, 'c'))
        self.assertEqual(p.hand.size(), 1)

    def test_draw(self):
        t = GinTable()
        p = GinPlayer()
        p.sit_at_table(t)

        self.assertEqual(p.hand.size(), 0)
        p.draw()
        self.assertEqual(p.hand.size(), 1)
        p.draw()
        self.assertEqual(p.hand.size(), 2)
        p.draw()
        p.draw()
        p.draw()
        p.draw()
        p.draw()
        p.draw()
        p.draw()
        p.draw()
        p.draw()
        self.assertEqual(p.hand.size(), 11)

        # ensure we cannot hold more than 11 cards
        self.assertRaises(DrawException, p.draw)

    def test_consult_strategy(self):
        strat = MockGinStrategy()
        p = GinPlayer(strat)

        # ensure the mock strategy give us exactly one action to perform
        self.assertEqual(False, p.action)
        p.consult_strategy()
        self.assertEqual('DISCARD', p.action[0])
        self.assertEqual(0, p.action[1])

    def test_execute_strategy_discard(self):
        strat = MockGinStrategy(['DISCARD', 0])
        p = GinPlayer(strat)

        # monkey-load a card into the player's hand
        p.hand.add(4, 'c')

        # run the strategy, which should cause us to discard our first card
        p.consult_strategy()
        p.execute_strategy()
        self.assertEqual(0, p.hand.size())

    def test_execute_strategy_draw(self):
        strat = MockGinStrategy(['DRAW'])
        p = GinPlayer(strat)

        # monkey-patching in a table
        p.table = GinTable()

        # ensure the player picks up the card from the top of the deck.
        topcard = p.table.deck.cards[-1]
        self.assertEqual(0, p.hand.size())
        self.assertEqual(52, len(p.table.deck.cards))

        p.consult_strategy()
        p.execute_strategy()

        self.assertEqual(1, p.hand.size())
        self.assertTrue(p.hand._contains_card(topcard.rank, topcard.suit))
        self.assertEqual(51, len(p.table.deck.cards))

    def test_execute_strategy_pickup_discard(self):
        strat = MockGinStrategy(['PICKUP-DISCARD'])
        p = GinPlayer(strat)

        # monkey-patching in a table and a discard pile of depth 3
        p.table = GinTable()
        p.table.discard_pile.append(p.table.deck.cards.pop())
        p.table.discard_pile.append(p.table.deck.cards.pop())
        p.table.discard_pile.append(p.table.deck.cards.pop())

        # ensure the player picks up the card from the top of the discard pile
        topcard = p.table.discard_pile[-1]
        self.assertEqual(0, p.hand.size())
        self.assertEqual(49, len(p.table.deck.cards))

        p.consult_strategy()
        p.execute_strategy()

        self.assertEqual(1, p.hand.size())
        self.assertTrue(p.hand._contains_card(topcard.rank, topcard.suit))
        self.assertEqual(49, len(p.table.deck.cards))

    def test_execute_strategy_knock(self):
        pass

    def test_execute_strategy_knock_gin(self):
        pass

    def test_take_turn(self):
        t = GinTable()
        p1 = GinPlayer()
        p2 = GinPlayer()
        p1.sit_at_table(t)
        p2.sit_at_table(t)
        # a player's hand should change after the first turn
        pass

    def test_pickup_discard(self):
        t = GinTable()
        p = GinPlayer()
        p.sit_at_table(t)

        # monkey-patch a card into the discard pile
        t.discard_pile.append(GinCard(4, 'c'))

        # a player's hand should change after picking up a discard
        size_before = p.hand.size()
        p.pickup_discard()
        size_after = p.hand.size()
        self.assertNotEqual(size_before, size_after)
        self.assertTrue(p.hand._contains_card(4, 'c'))

    def test_discard_card(self):
        t = GinTable()
        p = GinPlayer()
        p.sit_at_table(t)

        # ensure our hand is empty
        self.assertEqual(0, p.hand.size())

        # draw a card and ensure we're holding it
        card = p.draw()
        self.assertEqual(1, p.hand.size())

        # discard it and ensure we have 0 cards in hand, and that it is on top of the discard pile
        p.discard_card(card)
        self.assertEqual(0, p.hand.size())
        self.assertEqual(card, t.discard_pile.pop())

    def test_knock(self):
        pass


