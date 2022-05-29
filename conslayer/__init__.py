# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Patrick Michl
# This file is part of Console Slayer, https://github.com/fishroot/conslayer
#
"""Console Slayer.

Description:
    Console Slayer (conslayer) is a simple console-based hack and slash game.
    The player commands a hero to kill monsters by using console commands.

"""
__version__ = '1.0.0'
__status__ = 'Development'
__description__ = 'Console based hack and slash game'
__license__ = 'MIT'
__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__maintainer__ = 'Patrick Michl'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

# For conveniance import all classes to toplevel of conslayer package
from conslayer.arena import Arena, Guardian
from conslayer.combatant import Combatant, CombatantDict, Hero, Monster
from conslayer.console import MessageQueue

def main() -> None:
    """Entrypoint for conslayer."""

    stdout = MessageQueue()

    # Create arena and add hero
    arena = Arena()
    arena.add("hero")

    # Create guardian and let the guardian watch the arena
    guardian = Guardian()
    guardian.watch(arena)

    # Start the game
    stdout.print()

    while True:
        command = input("> ").strip().lower()

        if command == "exit":
            break
        elif command[:4] == "add ":
            arena.add(command[4:].strip())
        elif command == "start":
            arena.start_fight()
        elif command == "stop":
            arena.stop_fight()
        elif command[:7] == "attack ":
            arena["hero"].attack(command[7:].strip())
        elif command == "help":
            stdout.queue("Available commands:")
            stdout.queue("  'add <name>': Add a combatant to the arena")
            stdout.queue("  'start': Start the fight")
            stdout.queue("  'attack <monster>': Attack the monster")
            stdout.queue("  'stop': Stop the fight")
            stdout.queue("  'help': Show this help message")
            stdout.queue("  'about': Show application version")
            stdout.queue("  'exit': Exit the game")
        elif command == "about":
            stdout.queue(f"Console Slayer v{__version__}")
        elif command == "":
            pass
        else:
            stdout.queue(f"Unknown command. Type 'help' for a list of available commands.")

        stdout.print()

# Run main() if this file is executed directly
if __name__ == '__main__':
    main()