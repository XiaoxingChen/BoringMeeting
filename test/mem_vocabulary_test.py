import unittest
import sys
sys.path.append("../")
from mem_word import *

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_queue_top(self):
        pbs = []
        pbs.append(POSBlock("haha", [WordDefBlock("a", "b", "c")]))
        pbs.append(POSBlock("ddd", [WordDefBlock("a", "b", "d")]))
        mem_words = []
        mem_words.append(MemWord("word1", 3, pbs, "ddd"))
        mem_words.append(MemWord("word2", 3.1, pbs, "ccc"))
        voc = MemVocabulary(mem_words)
        print(voc.top_mem())



if __name__ == '__main__':
    unittest.main()