``` puml
class Guardian
{
    +arena : Arena
    +watch() : void
}

class Arena
{
    +state : List[dict]: 
    +heroes : List[Hero]
    +monsters : List[Monster]
    --
    +add() : void
    +remove() : void
    +start(): void
    +stop(): void
    +record_attack() : void
}

abstract class Combatant
{
    +state : dict
    +kind : type
    +name : str
    +health : int
    +damage : int
    +interval : float
    --
    +attack() : void
    +get_weakened() : void
}

class Hero
{
    +state : dict
    +kind : type
    +name : str
    +health : int
    +damage : int
    --
    +attack() : void
}

class Monster
{
    +state : dict
    +kind : type
    +name : str
    +health : int
    +damage : int
    +interval : float
    --
    +attack() : void
}

class MessageQueue
{
    +silent : bool
    --
    +queue() : void
    +flush() : void
    +print() : void
}

class CombatantDict
{
    -__items: list
    --
    +get() : list
}

Combatant <-- Monster: implement
Combatant <-- Hero: implement

CombatantDict <-- Combatant : bind

Guardian "1" --> "1" Arena : subscribe
Arena "1" *-> "n" Combatant : subscribe

Arena <-- Combatant : bind

Arena "1" --> "1" MessageQueue : bind
Guardian "1" --> "1" MessageQueue : bind
```