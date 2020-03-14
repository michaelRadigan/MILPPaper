from unittest import TestCase
from mpsParser import *


class MpsParser(TestCase):

    def test_foo(self):
        foo = parse("../../enlight9.mps")
        print("Hello")