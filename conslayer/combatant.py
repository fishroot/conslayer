# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Patrick Michl
# This file is part of Console Slayer, https://github.com/fishroot/conslayer
#
"""Combatant management."""

__copyright__ = '2022 Patrick Michl'
__license__ = 'MIT'
__docformat__ = 'google'
__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

from typing import Any, List, Optional
from abc import ABC

import reactivex as rx
import conslayer

#
# Combatant
#

class Combatant(rx.subject.BehaviorSubject, ABC):
    """Combatant base class.

    Abstract base class for all combatant classes. Stores individual combatant
    states and propagates state changes by using the following design patterns:
        (1) Behaviour Subject pattern for concurrent observability
        (2) State pattern for combatant state determination

    Args:
        kind (type): Kind of the combatant (conslayer.Hero or conslayer.Monster)
        name (str): Name of the combatant
        health (int): Health of the combatant
        damage (int): Health damage points an attack of the combatant causes
        interval (float, optional): Interval between attacks in seconds

    Attributes:
        kind (readonly, type): Kind of the combatant (conslayer.Hero or conslayer.Monster)
        name (readonly, str): Name of the combatant
        health (readonly, int): Health of the combatant
        damage (readonly, int): Health damage points an attack of the combatant causes
        interval (readonly, float): Interval between attacks in seconds
        state (readonly, dict): Current state of the combatant

    Raises:
        TypeError: If any of the arguments has the wrong type
        ValueError: If any of the arguments has an invalid value

    """

    __name: str
    __kind: type
    __health: int
    __damage: int
    __interval: Optional[float]

    @property
    def name(self) -> str: 
        return self.__name

    @property
    def kind(self) -> type:
        return self.__kind

    @property
    def health(self) -> int:
        return self.__health

    @property
    def damage(self) -> int:
        return self.__damage

    @property
    def interval(self) -> Optional[float]:
        return self.__interval

    @property
    def state(self) -> dict:
        return self.__getstate__()

    def __init__(self, kind: type, name: str, health: int, damage: int, interval: Optional[float] = None) -> None:

        # Check argument types
        if not isinstance(name, str):
            raise TypeError("Argument 'name' requires type 'str'")
        if not isinstance(health, int):
            raise TypeError("Argument 'health' requires type 'int'")
        if not isinstance(damage, int):
            raise TypeError("Argument 'damage' requires type 'int'")
        if interval is not None and not isinstance(interval, float):
            raise TypeError("Argument 'interval' requires type 'float'")
        
        # Check argument values
        if health < 0:
            raise ValueError("Argument 'health' requires to be positive")
        if damage < 0:
            raise ValueError("Argument 'damage' requires to be positive")
        if interval is not None and interval < 0:
            raise ValueError("Argument 'interval' requires to be positive or None")
        
        # Initialize attributes
        self.__kind = kind
        self.__name = name
        self.__health = health
        self.__damage = damage
        self.__interval = interval

        # Initialize superclass
        super().__init__(self.state)

    def __getstate__(self) -> dict:
        return {
            'kind': self.__kind,
            'name': self.__name,
            'health': self.__health,
            'damage': self.__damage,
            'interval': self.__interval
        }

    def attack(self, name: str) -> None:
        """Attack another combatant
        
        Args:
            name (str): Name of the combatant to attack

        """

        arena = conslayer.Arena()
        stdout = conslayer.MessageQueue()

        if not name in arena:
            stdout.queue(f"{name} is not in arena.")
            return
        
        arena.record_attack(self, arena[name])

    def get_weakened(self, damage: int) -> None:
        """Get weakened by damage points
        
        Args:
            damage (int): Damage points to weaken by

        """

        self.__health = max(0, self.__health - damage)
        self.on_next(self.state)

#
# Monster
#

class Monster(Combatant):
    """Monster class.

    Combatant class used to store individual monster states and propagate
    state changes by using the following design patterns:
        (1) Behaviour Subject pattern for concurrent observability
        (2) State pattern for monster state determination

    Args:
        name (str): Name of the monster
        health (int): Health of the monster
        damage (int): Health damage points an attack of the monster causes
        interval (int): Interval between attacks in seconds

    Attributes:
        name (str, readonly): Name of the monster
        health (int, readonly): Health of the monster
        damage (int, readonly): Health damage points an attack of the monster causes
        interval (float, readonly): Interval between attacks in seconds

    Raises:
        ValueError: Monster name cannot be 'hero'

    """
    def __init__(self, name: str, health: int, damage: int, interval: int) -> None:

        # Check argument values
        if name == "hero":
            raise ValueError("Monster name cannot be 'hero'")

        super().__init__(Monster, name, health, damage, interval)

#
# Hero
#

class Hero(Combatant):
    """Hero class.

    Combatant class used to store individual heroes states and propagate
    state changes by using the following design patterns:
        (1) Behaviour Subject pattern for concurrent observability
        (2) State pattern for hero state determination

    Args:
        health (int): Health of the hero
        damage (int): Health damage points an attack of the hero causes

    Attributes:
        health (int, readonly): Health of the hero
        damage (int, readonly): Health damage points an attack of the hero causes

    """
    def __init__(self, health: int, damage: int) -> None:
        super().__init__(Hero, "hero", health, damage)

#
# CombatantDict
#

class CombatantDict(dict):
    """CombatantDict class.
    
    Stores known combatant properties using the following patterns:
        (1) Singleton pattern for application global availability
        (2) Iterable pattern for iteration over all combatant properties

    """

    __instance: Optional['CombatantDict'] = None
    __initialized: bool = False
    __items: List[Any] = [
        ("hero", [Hero, 40, 2]),
        ("dragon", [Monster, "dragon", 20, 3, 2.0]),
        ("orc", [Monster, "orc", 7, 1, 1.5]),
    ]

    def __new__(cls) -> 'CombatantDict':
        if cls.__instance is None:
            cls.__instance = dict.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not self.__initialized:
            super().__init__(self.__items)
            self.__initialized = True
