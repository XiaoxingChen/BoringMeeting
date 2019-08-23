from vocabulary_cui import PushToLocalGlossary
from vocabulary_cui import ConcurrentInitMemWords

class LocalGlossary(object):
    def __init__(self, voc_path):
        self.voc_path = voc_path

    def GetMemWordQueue(self, words):
        inexistent = self.GetInexistent(words)
        self.AddNew(inexistent)

    def GetInexistent(self, words):
        pass

    def AddNew(self, words):
        mem_words = ConcurrentInitMemWords(words)
        PushToLocalGlossary(mem_words)