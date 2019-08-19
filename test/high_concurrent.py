import unittest
import sys
sys.path.append("../")
from vocabulary_trainer import *

class TestConcurrentMethods(unittest.TestCase):
    def test_concurrent(self):
        online_mem_words = ConcurrentInitMemWords(["hello"] * 500)



if __name__ == '__main__':
    unittest.main()