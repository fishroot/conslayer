# -*- coding: utf-8 -*-
# Copyright (C) 2022 Patrick Michl
# This file is part of Console Slayer, https://github.com/fishroot/conslayer
"""Testcases for combatant management."""

__copyright__ = '2022 Patrick Michl'
__license__ = 'MIT'
__docformat__ = 'google'
__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

import unittest
import conslayer

class CombatantTest(unittest.TestCase):
    def test_init_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        combatant = conslayer.Combatant(conslayer.Hero, "hero", 10, 5, 1.)
        self.assertIsInstance(combatant, conslayer.Combatant)
        self.assertEqual(combatant.kind, conslayer.Hero)
        self.assertEqual(combatant.name, "hero")
        self.assertEqual(combatant.health, 10)
        self.assertEqual(combatant.damage, 5)
        self.assertEqual(combatant.interval, 1.)

    def test_init_orc(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        combatant = conslayer.Combatant(conslayer.Monster, "orc", 10, 5, 1.)
        self.assertIsInstance(combatant, conslayer.Combatant)
        self.assertEqual(combatant.kind, conslayer.Monster)
        self.assertEqual(combatant.name, "orc")
        self.assertEqual(combatant.health, 10)
        self.assertEqual(combatant.damage, 5)
        self.assertEqual(combatant.interval, 1.)
    
    def test_init_dragon(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        combatant = conslayer.Combatant(conslayer.Monster, "dragon", 10, 5, 1.)
        self.assertIsInstance(combatant, conslayer.Combatant)
        self.assertEqual(combatant.kind, conslayer.Monster)
        self.assertEqual(combatant.name, "dragon")
        self.assertEqual(combatant.health, 10)
        self.assertEqual(combatant.damage, 5)
        self.assertEqual(combatant.interval, 1.)

    def test_attack_hero_orc(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("orc")
        prev_health = arena["orc"].health
        arena.start_fight()
        arena["hero"].attack("orc")
        arena.stop_fight()
        next_health = arena["orc"].health
        self.assertEqual(prev_health - next_health, arena["hero"].damage)

    def test_attack_hero_dragon(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("dragon")
        prev_health = arena["dragon"].health
        arena.start_fight()
        arena["hero"].attack("dragon")
        arena.stop_fight()
        next_health = arena["dragon"].health
        self.assertEqual(prev_health - next_health, arena["hero"].damage)

    def test_attack_orc_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("orc")
        prev_health = arena["orc"].health
        arena.start_fight()
        arena["hero"].attack("orc")
        arena.stop_fight()
        next_health = arena["orc"].health
        self.assertEqual(prev_health - next_health, arena["hero"].damage)

    def test_attack_dragon_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("dragon")
        prev_health = arena["hero"].health
        arena.start_fight()
        arena["dragon"].attack("hero")
        arena.stop_fight()
        next_health = arena["hero"].health
        self.assertEqual(prev_health - next_health, arena["dragon"].damage)

    def test_attack_orc_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        arena.add("orc")
        prev_health = arena["hero"].health
        arena.start_fight()
        arena["orc"].attack("hero")
        arena.stop_fight()
        next_health = arena["hero"].health
        self.assertEqual(prev_health - next_health, arena["orc"].damage)

    def test_get_weakened_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("hero")
        prev_health = arena["hero"].health
        arena["hero"].get_weakened(5)
        next_health = arena["hero"].health
        self.assertEqual(prev_health - next_health, 5)
        arena["hero"].get_weakened(next_health)
        self.assertEqual(arena["hero"].health, 0)

    def test_get_weakened_dragon(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("orc")
        prev_health = arena["orc"].health
        arena["orc"].get_weakened(5)
        next_health = arena["orc"].health
        self.assertEqual(prev_health - next_health, 5)
        arena["orc"].get_weakened(next_health)
        self.assertEqual(arena["orc"].health, 0)

    def test_get_weakened_orc(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        arena = conslayer.Arena()
        arena.add("dragon")
        prev_health = arena["dragon"].health
        arena["dragon"].get_weakened(5)
        next_health = arena["dragon"].health
        self.assertEqual(prev_health - next_health, 5)
        arena["dragon"].get_weakened(next_health)
        self.assertEqual(arena["dragon"].health, 0)

class MonsterTest(unittest.TestCase):
    def test_init_orc(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        monster = conslayer.Monster("orc", 10, 5, 1.)
        self.assertIsInstance(monster, conslayer.Monster)
        self.assertEqual(monster.kind, conslayer.Monster)
        self.assertEqual(monster.name, "orc")
        self.assertEqual(monster.health, 10)
        self.assertEqual(monster.damage, 5)
        self.assertEqual(monster.interval, 1.)

    def test_init_dragon(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        monster = conslayer.Monster("dragon", 10, 5, 1.)
        self.assertIsInstance(monster, conslayer.Monster)
        self.assertEqual(monster.kind, conslayer.Monster)
        self.assertEqual(monster.name, "dragon")
        self.assertEqual(monster.health, 10)
        self.assertEqual(monster.damage, 5)
        self.assertEqual(monster.interval, 1.)

class HeroTest(unittest.TestCase):
    def test_init_hero(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        hero = conslayer.Hero(10, 5)
        self.assertIsInstance(hero, conslayer.Hero)
        self.assertEqual(hero.kind, conslayer.Hero)
        self.assertEqual(hero.name, "hero")
        self.assertEqual(hero.health, 10)
        self.assertEqual(hero.damage, 5)
        self.assertEqual(hero.interval, None)

class CombatantDictTest(unittest.TestCase):
    def test_new(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        combatants_a = conslayer.CombatantDict()
        combatants_b = conslayer.CombatantDict()
        self.assertTrue(combatants_a is combatants_b)

    def test_init(self):
        conslayer.MessageQueue().silent = True
        conslayer.Arena().clear()
        combatants = conslayer.CombatantDict()
        self.assertIsInstance(combatants, conslayer.CombatantDict)
        self.assertIn("hero", combatants)
        self.assertIn("orc", combatants)
        self.assertIn("dragon", combatants)


if __name__ == '__main__':
    unittest.main()
