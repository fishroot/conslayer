# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Patrick Michl
# This file is part of Console Slayer, https://github.com/fishroot/conslayer
"""Arena management."""

__copyright__ = '2022 Patrick Michl'
__license__ = 'MIT'
__docformat__ = 'google'
__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

from typing import Dict, Iterator, List, Optional, OrderedDict

import reactivex as rx
import conslayer

#
# Arena
#

class Arena(rx.subject.BehaviorSubject):
    """Arena Class.

    Description:
        Administer the states of combatants and publish global state changes.

    Attributes:
        state (readonly, OrderedDict): Global state of all combatants.
        heroes (readonly, OrderedDict): All heroes in arena.
        monsters (readonly, OrderedDict): All monsters in arena.

    Design Patterns:
        Singleton, Registry, Behaviour Subject

    """

    __instance: Optional['Arena'] = None
    __initialized: bool = False
    __started: bool = False
    __registry: OrderedDict[str, 'conslayer.Combatant'] = OrderedDict()
    __listener: Dict[str, rx.abc.disposable.DisposableBase] = {}
    __scheduler: Dict[str, rx.abc.disposable.DisposableBase] = {}

    @property
    def state(self) -> List[dict]:
        """Get global state of all combatants."""
        return self.__getstate__()

    @property
    def heroes(self) -> List['conslayer.Hero']:
        """Get list of heroes"""
        return [
            combatant for combatant in self.__registry.values()
            if isinstance(combatant, conslayer.Hero)
        ]

    @property
    def monsters(self) -> List['conslayer.Monster']:
        """Get list of monsters"""
        return [
            combatant for combatant in self.__registry.values()
            if isinstance(combatant, conslayer.Monster)
        ]

    def __new__(cls) -> 'Arena':
        if cls.__instance is None:
            cls.__instance = super(Arena, cls).__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        if not self.__initialized:
            super(Arena, self).__init__(self.state)
            conslayer.MessageQueue().queue("Welcome to the arena! Type 'help' for more information.")
            conslayer.MessageQueue().print()
            self.__initialized = True

    def __getstate__(self) -> List[dict]:
        return [combatant.state for combatant in self.__registry.values()]

    def __contains__(self, name: str) -> bool:
        return name in self.__registry

    def __getitem__(self, name: str) -> 'conslayer.Combatant':
        return self.__registry[name]

    def __len__(self) -> int:
        return len(self.__registry)

    def __iter__(self) -> Iterator['conslayer.Combatant']:
        for combatant in self.__registry.values():
            yield combatant

    def add(self, name: str) -> None:
        """Add combatant to arena.

        Args:
            combatant (Combatant): Combatant to add to arena.

        Raises:
            KeyError: Combatant already in arena.

        """

        # Check argument type
        if not isinstance(name, str):
            raise TypeError("Argument 'name' requires type 'str'")

        # Bind message queue
        stdout = conslayer.MessageQueue()

        # Check if combatant is already in arena
        name = name.lower()
        if name in self.__registry:
            stdout.queue(f"{name} is already in arena.")
            return

        # Check if combatant is known
        if name not in conslayer.CombatantDict():
            stdout.queue(f"{name} is not known.")
            return

        # Get combatant
        args = conslayer.CombatantDict()[name]
        combatant = args[0](*args[1:])

        # Add combatant to registry
        self.__registry[combatant.name] = combatant

        # Subscribe to combatant state changes
        listener = combatant.subscribe(lambda _: self.on_next(self.state))

        # Add subscription to listeners
        self.__listener[combatant.name] = listener

        # Create message
        stdout.queue(f"{combatant.name.title()} enters arena.")

    def remove(self, name: str) -> None:
        """Remove combatant from arena.
        
        Args:
            name (str): Name of combatant to remove.
        
        Raises:
            KeyError: Combatant not found.

        """

        # Check argument type
        if not isinstance(name, str):
            raise TypeError("Argument 'name' requires type 'str'")

        # Bind message queue
        stdout = conslayer.MessageQueue()

        # Check if combatant is in arena
        name = name.lower()
        if name not in self.__registry:
            stdout.queue(f"{name.title()} is not in arena.")
            return

        # Create message
        stdout.queue(f"{name.title()} is removed from arena.")

        # Dispose listener
        if name in self.__listener:
            self.__listener[name].dispose()
            del self.__listener[name]

        # Dispose scheduler
        if name in self.__scheduler:
            self.__scheduler[name].dispose()
            del self.__scheduler[name]

        # Remove combatant from registry
        del self.__registry[name]
        self.on_next(self.state)

    def clear(self) -> None:
        """Remove all combatants from arena."""

        # Remove all combatants
        for name in self.__registry:

            # Dispose listener
            if name in self.__listener:
                self.__listener[name].dispose()
                del self.__listener[name]

            # Dispose scheduler
            if name in self.__scheduler:
                self.__scheduler[name].dispose()
                del self.__scheduler[name]

        self.__registry.clear()

    def start_fight(self, message: Optional[str] = None) -> None:
        """Start fight.

        Description:
            Start fight between combatants.

        Args:
            message (optional, str): Message to print.

        """

        stdout = conslayer.MessageQueue()

        # Check if fight is already started
        if self.__started:
            stdout.queue("Fight already started.")
            return

        # Check if there is a hero in arena
        if len(self.heroes) == 0:
            stdout.queue("No hero in arena. Fight cannot start.")
            return

        # Check if there is a monster in arena
        if len(self.monsters) == 0:
            stdout.queue("No monsters in arena. Fight cannot start.")
            return

        # Define attack builder
        def build_attack(monster: conslayer.Monster) -> None:
            arena = conslayer.Arena()
            def attack(value):
                if monster.health <= 0: return value
                if not "hero" in arena: return value
                if arena["hero"].health <= 0: return value
                monster.attack("hero")
                return value
            return attack

        # Create attack scheduler
        for monster in self.monsters:
            scheduler = rx.scheduler.EventLoopScheduler()
            attack = build_attack(monster)
            obs = scheduler.schedule_periodic(monster.interval, attack)
            self.__scheduler[monster.name] = obs

        # Start fight
        self.__started = True
        stdout.queue("Fight started!")
        if message is not None:
            stdout.queue(message)

    def stop_fight(self, message: Optional[str] = None) -> None:
        """Stop fight.

        Description:
            Stop fight between combatants.

        Args:
            message (optional, str): Message to print.

        """

        # Bind message queue
        stdout = conslayer.MessageQueue()

        # Check if fight has already started
        if not self.__started:
            stdout.queue("Fight has not yet started.")
            return

        # Remove Schedulers
        for scheduler in self.__scheduler.values():
            scheduler.dispose()
        self.__scheduler.clear()

        # Stop fight
        self.__started = False
        stdout.queue("Fight stopped!")
        if message is not None:
            stdout.queue(message)

    def record_attack(self, attacker: 'conslayer.Combatant', target: 'conslayer.Combatant') -> None:
        """Record attack in global registry.
        
        Args:
            attacker (Combatant): Attacker
            target (Combatant): Target
        
        """

        # Check argument types
        if not isinstance(attacker, conslayer.Combatant):
            raise TypeError("Argument 'attacker' requires type 'Combatant'")
        if not isinstance(target, conslayer.Combatant):
            raise TypeError("Argument 'target' requires type 'Combatant'")

        # Check if attacker and target are in arena
        if attacker.name not in self.__registry:
            raise KeyError(f"Attacker '{attacker.name}' is not known in arena")
        if target.name not in self.__registry:
            raise KeyError(f"Target '{target.name}' is not known in arena")

        # Check if attacker and target are alive
        if attacker.health <= 0:
            raise Exception(f"Attacker '{attacker.name}' is already dead")
        if target.health <= 0:
            raise Exception(f"Target '{target.name}' is already dead")

        # Bind message queue
        stdout = conslayer.MessageQueue()

        # Check if fight is started
        if not self.__started:
            stdout.queue("Fight has not yet started.")
            return

        # Create message
        health = max(0, target.health - attacker.damage)
        attacker_name = attacker.name.title()
        target_name = target.name.title()
        if health > 0:
            message = f"{attacker_name} hits {target_name}. {target_name} health is {health}."
        else:
            message = f"{attacker_name} killed {target_name}."
        stdout.queue(message)

        # Update health of target
        target.get_weakened(attacker.damage)

        # Emit new global state
        self.on_next(self.state)

#
# Guardian
#

class Guardian(rx.Observer):
    """Guardian class.

    Description:
        Guardian class, used to observe and evaluate arena state changes.
        If a monster dies, the guardian will remove the monster from the arena.
        If all monsters are dead, the guardian will stop the fight and pronounce the player the winner.
        If the hero dies, the guardian will stop the fight pronounce the monsters the winner.

    Design Patterns:
        Singleton, Observer

    """

    __instance: Optional['Guardian'] = None

    def __new__(cls) -> 'Guardian':
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def watch(self, arena: 'conslayer.Arena') -> None:
        """Observe arena state changes.
        
        Args:
            arena (Arena): Arena to observe.
        
        """
        arena.subscribe(self)

    def on_next(self, table: List[dict]):
        """Evaluate arena state changes.

        Args:
            table (List[dict]): Arena state.

        """

        # Bind message queue
        stdout = conslayer.MessageQueue()

        # Bind arena
        arena = conslayer.Arena()

        # Evaluate combatants health states
        heroes = 0
        monsters = 0
        remove = []
        for row in table:
            if row['health'] <= 0:
                remove.append(row['name'])
            elif row['kind'] is conslayer.Monster:
                monsters += 1
            elif row['kind'] is conslayer.Hero:
                heroes += 1

        # Remove combatants
        for name in remove:
            arena.remove(name)

        # Check if all monsters are dead
        if remove and monsters == 0:
            arena.stop_fight("All monsters are dead. Hero wins!")
            stdout.print()
            return
        
        # Check if all heroes are dead
        if remove and heroes == 0:
            arena.stop_fight("Hero is dead. Monsters win!")
            stdout.print()
            return
