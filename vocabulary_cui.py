from lxml import html
import logging
import requests
import multiprocessing as mp
from mem_word import MemWordQueue
from vocabulary_path import VocabularyPath
from mem_word import MemWord
from mem_word import HyperTextMemWord
from mem_word import TerminalVis
import os
from sql_glossary import SQLGlossary
import yaml
import readline
from functools import partial

# page = requests.get('https://www.lexico.com/en/definition/eleemosynary')
# tree = html.fromstring(page.content)
# buyers = tree.xpath('//div[@class="senseInnerWrapper"]/p')
# print(buyers[0].text_content())

def ProcessFunc(w, q, glossary_filename, total_words):
    hyper_text_mem_w = None
    for i in range(3):
        try:
            hyper_text_mem_w = HyperTextMemWord.OnlineConstruct(w)
        except:
            print('Retry of word: {}, {}th'.format(w, i+1))
            continue
        else:
            break
    if hyper_text_mem_w is None:
        print('word: "{}" failed'.format(w))
        return
    q.put(hyper_text_mem_w.mem_word)
    db = SQLGlossary(glossary_filename)
    db.ReplaceWord(w, yaml.dump(hyper_text_mem_w.mem_word), 3., hyper_text_mem_w.audio)
    print("load {}/{}".format(q.qsize(), total_words), end='\r')

# def InitVocabularyOnlineConcurrent(words):
def ConcurrentInitMemWords(words, voc_path):
    import time
    print("Construct Vocabulary !")
    manager = mp.Manager()
    q = manager.Queue()

    with mp.Pool(30) as pool:
        pool.map(partial(ProcessFunc, q=q, glossary_filename=voc_path, total_words=len(words)), words)

    mem_words = []
    while q.qsize() > 0:
        mem_words.append(q.get())

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

def GetInitializedState(words, glossary_filename):
    db = SQLGlossary(glossary_filename)
    exists = db.Exists(words)
    initialized_words = [words[i] for i in range(len(words)) if exists[i]]
    uninitialized_words = [words[i] for i in range(len(words)) if not exists[i]]
    print("{}/{} words exist!".format(len(initialized_words), len(words)))
    return initialized_words, uninitialized_words

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

def GetDefinitions(words, glossary_filename):
    db = SQLGlossary(glossary_filename)
    return db.FetchDefinitions(words)

class VocabularyCUI(object):

    def __init__(self, words, root_folder, vocabularies):
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.)
        print(TerminalVis.CLS)
        self.db_path = os.path.expanduser("~") + os.sep + ".glossary"
        self.vocab = MemWordQueue()
        self.repo_root = root_folder 
        self.log_file = root_folder + '/simple_recaller.log'
        logging.basicConfig(filename=self.log_file, format='[%(asctime)s]%(message)s', level=logging.INFO)
        initialized_words, uninitialized_words = GetInitializedState(words, self.db_path)
        ConcurrentInitMemWords(uninitialized_words, self.db_path)
        self.vocab.Push(GetDefinitions(words, self.db_path))
        logging.info('loggin')
        for voc in vocabularies:
            logging.info('[vocabulary: {}]'.format(voc))
        logging.info('[totally {} words]'.format(len(words)))

    def PrintHeadVisWord(self, w):
        print(TerminalVis.CLS)
        print(TerminalVis.VerticalSpacing(10))
        print((w).center(100))

    def Run(self):
        while True:
            self.PrintHeadVisWord()
            input()
            self.Pronounce(self.vocab.HeadWord().word, repeat=3)
            while True:
                self.PrintHeadVisWord()
                print(self.vocab.HeadWord())
                level = input(TerminalVis.MemLevel())
                try:
                    self.vocab.Update(float(level))
                    logging.info("word=%s mem_level=%s", self.vocab.HeadWord().word, level)
                except ValueError:
                    pass
                else:
                    break

    def RunSpell(self):
        while True:
            while True:
                self.PrintHeadVisWord('_' * 10)
                print(self.vocab.HeadWord().VisMaskedString())
                word = input('spell check: ')
                if word == self.vocab.HeadWord().word:
                    break
                elif word == ".s": #speak
                    self.Pronounce(self.vocab.HeadWord().word, repeat=3)
                elif word == ".w": #word
                    input(self.vocab.HeadWord().word)
                elif word == ".q": #quit
                    self.Close()
                    quit()

            while True:
                self.Pronounce(self.vocab.HeadWord().word, repeat=3)
                self.PrintHeadVisWord(self.vocab.HeadWord().vis_word)
                print(self.vocab.HeadWord())
                print("Max cost: {:.3f}".format(self.vocab.HeadWord().mem_level))
                level = input(TerminalVis.MemLevel())
                logging.info("word=%s mem_level=%s", self.vocab.HeadWord().word, level)
                try:
                    self.vocab.Update(float(level))
                except ValueError:
                    pass
                else:
                    break

    def Close(self):
        print('\nExit, storing database ...')
        logging.info('loggout')
        db = SQLGlossary(self.db_path)
        for w in self.vocab.RawData():
            db.UpdateMemLevel(w.word, w.mem_level)
        
        os.chdir(self.repo_root)
        os.system('git stage {}'.format(self.log_file))
        os.system('git commit -m "Modify: auto commit by tc_trainer"')

    def Pronounce(self, w, repeat=1):
        import pygame
        import io
        db = SQLGlossary(self.db_path)
        audio = db.FetchPronounce(w)
        if audio is None:
            return
        inmemoryfile = io.BytesIO(audio)
        pygame.mixer.music.load(inmemoryfile)
        pygame.mixer.music.play(repeat-1)

if __name__ == "__main__":
    vocabulary = ['detection'] * 10
    voc = ConcurrentInitVocabulary(vocabulary)
    #print(q.get())
    print(voc)


