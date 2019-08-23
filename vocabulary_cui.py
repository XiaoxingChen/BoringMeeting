from lxml import html
import requests
import multiprocessing as mp
from mem_word import MemVocabulary
from vocabulary_path import VocabularyPath
from mem_word import MemWord
from mem_word import TerminalVis
import os

# page = requests.get('https://www.lexico.com/en/definition/eleemosynary')
# tree = html.fromstring(page.content)
# buyers = tree.xpath('//div[@class="senseInnerWrapper"]/p')
# print(buyers[0].text_content())

def ProcessFunc(w, q, total_num, counter):
    mem_w = MemWord.OnlineConstruct(w)
    # mem_w = "test"
    q.put(mem_w)
    counter.value += 1
    print("load {}/{}".format(counter.value, total_num), end='\r')

# def InitVocabularyOnlineConcurrent(words):
def ConcurrentInitMemWords(words):
    import time
    print("Construct Vocabulary !")
    q = mp.Queue()
    counter = mp.Manager().Value('i', 0)
    ps = []
    for w in words:
        p = mp.Process(target=ProcessFunc, args=(w,q, len(words), counter))
        ps.append(p)
        p.start()

    mem_words = []

    while len(mem_words) < len(words):
        if q.qsize() > 0:
            mem_words.append(q.get())
        else:
            time.sleep(0.1)

    for p in ps:
        p.join()

    print("Vocabulary construction done!")
    return mem_words

def InitMemWordsFromLocal(words, glossary_filename):
    import yaml
    local_mem_words = None
    failure_return = ([], words)
    if not os.path.isfile(glossary_filename):
        print("no local glossary!")
        return failure_return

    with open(glossary_filename, 'r') as g:
        local_mem_words = yaml.load(g.read())

    if local_mem_words is None:
        print("local glossary empty!")
        return failure_return
    print("local glossary size: {}".format(len(local_mem_words)))
    word_gloss_map = {w: None for w in words}
    for mem_w in local_mem_words:
        if mem_w.word in words:
            word_gloss_map[mem_w.word] = mem_w
    # print(word_gloss_map)
    uninitialized_words = []#[k for k in word_gloss_map if word_gloss_map[k] is None]
    initialized_mem_words = []#[word_gloss_map[k] for k in word_gloss_map if word_gloss_map[k] is not None]
    for k in word_gloss_map:
        if word_gloss_map[k] is None:
            uninitialized_words.append(k)
        else:
            initialized_mem_words.append(word_gloss_map[k])

    print("uninitialized_words size: {}".format(len(uninitialized_words)))
    return initialized_mem_words, uninitialized_words


def PushToLocalGlossary(mem_words, glossary_filename):
    import yaml
    existed_glossary = mem_words
    if os.path.isfile(glossary_filename):
        with open (glossary_filename, 'r') as g:
            local_glossary = yaml.load(g.read())
            if local_glossary is not None:
                existed_glossary += local_glossary
    with open (glossary_filename, 'w') as g:
        g.write(yaml.dump(existed_glossary))

def

class VocabularyIncrementalInitializer(object):
    def __init__(self, path, words):
        self.path = path
        self.words = words

class VocabularyCUI(object):
    def __init__(self, words, root_folder):
        self.voc_path = VocabularyPath(root_folder)
        self.vocab = MemVocabulary()
        mem_words, uninitialized_words = InitMemWordsFromLocal(words, self.voc_path.glossary)
        online_mem_words = ConcurrentInitMemWords(uninitialized_words)
        print("words num: {}, {} from local, {} from online".format(len(words), len(mem_words), len(uninitialized_words)))
        mem_words += online_mem_words
        PushToLocalGlossary(online_mem_words, self.voc_path.glossary)
        self.vocab.Push(mem_words)

    def Run(self):
        while True:
            input((self.vocab.HeadWord().vis_word).center(100))
            print(self.vocab.HeadWord())
            while True:
                try:
                    level = input(TerminalVis.MemLevel())
                    print(TerminalVis.CLS)
                    print('\n' * 10)
                    self.vocab.Update(float(level))
                except ValueError:
                    pass
                else:
                    break


if __name__ == "__main__":
    vocabulary = ['detection'] * 10
    voc = ConcurrentInitVocabulary(vocabulary)
    #print(q.get())
    print(voc)


