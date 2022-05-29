# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Patrick Michl
# This file is part of Console Slayer, https://github.com/fishroot/conslayer
#
"""Testcases for arena management."""

__copyright__ = '2022 Patrick Michl'
__license__ = 'MIT'
__docformat__ = 'google'
__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

import unittest
import conslayer

class ArenaTest(unittest.TestCase):
    def test_new(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena_a = conslayer.MessageQueue()
        arena_b = conslayer.MessageQueue()
        self.assertTrue(arena_a is arena_b)

    def test_init(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        self.assertIsInstance(arena, conslayer.Arena)
        self.assertEqual(len(arena.state), 0)
        self.assertEqual(len(arena.heroes), 0)
        self.assertEqual(len(arena.monsters), 0)

    def test_state(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        self.assertEqual(len(arena.state), 1)
        self.assertEqual(arena.state[0]["kind"], conslayer.Hero)
        self.assertEqual(arena.state[0]["name"], "hero")
        self.assertTrue(arena.state[0]["health"] > 0)
        self.assertTrue(arena.state[0]["damage"] > 0)
        self.assertEqual(arena.state[0]["interval"], None)

    def test_heroes(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        self.assertEqual(len(arena.heroes), 1)
        self.assertEqual(arena.heroes[0].kind, conslayer.Hero)
        self.assertEqual(arena.heroes[0].name, "hero")
        self.assertTrue(arena.heroes[0].health > 0)
        self.assertTrue(arena.heroes[0].damage > 0)
        self.assertEqual(arena.heroes[0].interval, None)

    def test_monsters_orc(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("orc")
        self.assertEqual(len(arena.monsters), 1)
        self.assertEqual(arena.monsters[0].kind, conslayer.Monster)
        self.assertEqual(arena.monsters[0].name, "orc")
        self.assertTrue(arena.monsters[0].health > 0)
        self.assertTrue(arena.monsters[0].damage > 0)
        self.assertTrue(arena.monsters[0].interval > 0)

    def test_monsters_dragon(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("dragon")
        self.assertEqual(len(arena.monsters), 1)
        self.assertEqual(arena.monsters[0].kind, conslayer.Monster)
        self.assertEqual(arena.monsters[0].name, "dragon")
        self.assertTrue(arena.monsters[0].health > 0)
        self.assertTrue(arena.monsters[0].damage > 0)
        self.assertTrue(arena.monsters[0].interval > 0)

    def test_add_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        self.assertEqual(len(arena.heroes), 1)
        self.assertEqual(arena.heroes[0].kind, conslayer.Hero)
        self.assertEqual(arena.heroes[0].name, "hero")
        self.assertTrue(arena.heroes[0].health > 0)
        self.assertTrue(arena.heroes[0].damage > 0)
        self.assertEqual(arena.heroes[0].interval, None)

    def test_add_orc(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("orc")
        self.assertEqual(len(arena.monsters), 1)
        self.assertEqual(arena.monsters[0].kind, conslayer.Monster)
        self.assertEqual(arena.monsters[0].name, "orc")
        self.assertTrue(arena.monsters[0].health > 0)
        self.assertTrue(arena.monsters[0].damage > 0)
        self.assertTrue(arena.monsters[0].interval > 0)

    def test_add_dragon(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("dragon")
        self.assertEqual(len(arena.monsters), 1)
        self.assertEqual(arena.monsters[0].kind, conslayer.Monster)
        self.assertEqual(arena.monsters[0].name, "dragon")
        self.assertTrue(arena.monsters[0].health > 0)
        self.assertTrue(arena.monsters[0].damage > 0)
        self.assertTrue(arena.monsters[0].interval > 0)

    def test_clear(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("dragon")
        arena.add("orc")
        arena.clear()
        self.assertEqual(len(arena.state), 0)
        self.assertEqual(len(arena.heroes), 0)
        self.assertEqual(len(arena.monsters), 0)

    def test_remove_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        self.assertEqual(len(arena.heroes), 1)
        arena.remove("hero")
        self.assertEqual(len(arena.heroes), 0)

    def test_remove_dragon(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("dragon")
        self.assertEqual(len(arena.monsters), 1)
        arena.remove("dragon")
        self.assertEqual(len(arena.monsters), 0)

    def test_remove_orc(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("orc")
        self.assertEqual(len(arena.monsters), 1)
        arena.remove("orc")
        self.assertEqual(len(arena.monsters), 0)

    def test_start_fight(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("orc")
        prev_health = arena["orc"].health
        arena.start_fight()
        arena["hero"].attack("orc")
        arena.stop_fight()
        cur_health = arena["orc"].health
        self.assertEqual(prev_health - cur_health, arena["hero"].damage)

    def test_stop_fight(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("orc")
        prev_health = arena["orc"].health
        arena.start_fight()
        arena.stop_fight()
        arena["hero"].attack("orc")
        cur_health = arena["orc"].health
        self.assertEqual(prev_health - cur_health, 0)

    def test_record_attack(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("orc")
        hero = arena["hero"]
        orc = arena["orc"]
        prev_health = arena["orc"].health
        arena.start_fight()
        arena.record_attack(hero, orc)
        arena.stop_fight()
        cur_health = arena["orc"].health
        self.assertEqual(prev_health - cur_health, hero.damage)


class GuardianTest(unittest.TestCase):
    def test_new(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        guardian_a = conslayer.Guardian()
        guardian_b = conslayer.Guardian()
        self.assertTrue(guardian_a is guardian_b)

    def test_init(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        guardian = conslayer.Guardian()
        self.assertIsInstance(guardian, conslayer.Guardian)

    def test_watch(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("orc")
        self.assertEqual(len(arena.monsters), 1)
        guardian = conslayer.Guardian()
        guardian.watch(arena)
        arena.start_fight()
        for _ in range(5):
            arena["hero"].attack("orc")
        self.assertEqual(len(arena.monsters), 0)


if __name__ == '__main__':
    unittest.main()
