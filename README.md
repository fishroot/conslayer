# Console Slayer
*Console Slayer* is a simplistic console-based [hack and slash](https://en.wikipedia.org/wiki/Hack_and_slash) game.

## Getting Started
Console Slayer requires [Python](https://www.python.org) 3.7 or above. To install:

```bash
$ git clone https://github.com/fishroot/conslayer.git
$ pip install ./conslayer
```
## Dependencies
* [ReactiveX](https://github.com/ReactiveX/RxPY) >= 4

## Usage
```bash
$ conslayer
```

```
Welcome to the arena! Type 'help' for more information.
Hero enters arena.
> help
Available commands:
  'add <name>': Add a combatant to the arena (orc, dragon, hero)
  'start': Start the fight
  'attack <name>': Attack the monster
  'stop': Stop the fight
  'help': Show this help message
  'about': Show application version
  'exit': Exit the game
```

## Testing
```bash
$ git clone https://github.com/fishroot/conslayer.git
$ pip install ./conslayer
$ cd ./conslayer
$ python -m unittest discover -v
```
