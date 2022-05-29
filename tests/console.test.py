# -*- coding: utf-8 -*-
# Copyright (C) 2022 Patrick Michl
# This file is part of Console Slayer, https://github.com/fishroot/conslayer
"""Testcases for console management."""

__copyright__ = '2022 Patrick Michl'
__license__ = 'MIT'
__docformat__ = 'google'
__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

import unittest
import conslayer

class MessageQueueTest(unittest.TestCase):
    def test_new(self):
        conslayer.MessageQueue().silent = True
        stdout_a = conslayer.MessageQueue()
        stdout_b = conslayer.MessageQueue()
        self.assertTrue(stdout_a is stdout_b)

    def test_init(self):
        stdout = conslayer.MessageQueue()
        stdout.silent = True
        stdout.flush()
        self.assertIsInstance(stdout, conslayer.MessageQueue)
        self.assertEqual(stdout.silent, True)

    def test_silent(self):
        stdout = conslayer.MessageQueue()
        stdout.silent = True
        stdout.flush()
        self.assertEqual(stdout.silent, True)
        stdout.silent = False
        self.assertEqual(stdout.silent, False)

    def test_queue(self):
        stdout = conslayer.MessageQueue()
        stdout.silent = True
        stdout.flush()
        stdout.queue("Test")
        self.assertEqual(str(stdout), "Test")
        stdout.queue("Test")
        self.assertEqual(str(stdout), "Test\nTest")
        stdout.queue("Test")
        self.assertEqual(str(stdout), "Test\nTest\nTest")

    def test_flush(self):
        stdout = conslayer.MessageQueue()
        stdout.silent = True
        stdout.flush()
        stdout.queue("Test")
        self.assertEqual(str(stdout), "Test")
        stdout.flush()
        self.assertEqual(str(stdout), "")

    def test_print(self):
        stdout = conslayer.MessageQueue()
        stdout.silent = True
        stdout.flush()
        stdout.queue("Test")
        self.assertEqual(str(stdout), "Test")
        stdout.print()
        self.assertEqual(str(stdout), "Test")

if __name__ == '__main__':
    unittest.main()
