from typing import Any, List, Optional

import reactivex as rx
import conslayer

class Combatant(rx.subject.BehaviorSubject):
    """
    Combatant class.

    Description:
        Stores individual combatant states and publishes state changes.

    Attributes:
        kind (readonly, type): Kind of the combatant (conslayer.Hero or conslayer.Monster)
        name (readonly, str): Name of the combatant
        health (readonly, int): Health of the combatant
        damage (readonly, int): Health damage points an attack of the combatant causes
        interval (readonly, float): Interval between attacks in seconds
        state (readonly, dict): Current state of the combatant

    Design Patterns:
        Behaviour Subject

    """

    __name: str
    __kind: type
    __health: int
    __damage: int
    __interval: Optional[float]

    @property
    def name(self):
        return self.__name

    @property
    def kind(self):
        return self.__kind

    @property
    def health(self):
        return self.__health

    @property
    def damage(self):
        return self.__damage

    @property
    def interval(self):
        return self.__interval

    @property
    def state(self):
        return self.__getstate__()

    def __init__(self, kind: type, name: str, health: int, damage: int, interval: Optional[float] = None):

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

    def __getstate__(self):
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

    def get_weakened(self, damage: int):
        """Get weakened by damage points
        
        Args:
            damage (int): Damage points to weaken by

        """

        self.__health = max(0, self.__health - damage)
        self.on_next(self.state)

class Monster(Combatant):
    """
    Monster class.

    Description:
        Combatant subclass for mosnsters.

    Attributes:
        name (readonly, str): Name of the monster
        health (readonly, int): Health of the monster
        damage (readonly, int): Health damage points an attack of the monster causes
        interval (readonly, float): Interval between attacks in seconds

    Design Patterns:
        Behaviour Subject

    """
    def __init__(self, name: str, health: int, damage: int, interval: int):

        # Check argument values
        if name == "hero":
            raise Exception("Monster name cannot be 'hero'")

        super().__init__(Monster, name, health, damage, interval)

class Hero(Combatant):
    """
    Hero class.

    Description:
        Combatant subclass for heroes.

    Attributes:
        health (readonly, int): Health of the hero
        damage (readonly, int): Health damage points an attack of the hero causes

    Design Patterns:
        Behaviour Subject

    """
    def __init__(self, health: int, damage: int):
        super().__init__(Hero, "hero", health, damage)


class CombatantDict(dict):
    """
    CombatantDict class.
    
    Description:
        Stores a dictionary of combatants.

    Design Patterns:
        Singleton

    """

    __instance: Optional['CombatantDict'] = None
    __initialized: bool = False
    __items: List[Any] = [
        ("hero", [Hero, 40, 2]),
        ("dragon", [Monster, "dragon", 20, 3, 2.0]),
        ("orc", [Monster, "orc", 7, 1, 1.5]),
    ]

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = dict.__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            super().__init__(self.__items)
            self.__initialized = True