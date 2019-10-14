import readline
import logging
import sys
from colorama import Fore, Back, Style
from queue import PriorityQueue
import yaml
from test.gre_tc_filter import *
from lxml import html
import re
from mem_word import TerminalVis
import time

class TextCompletionLib(object):
    def __init__(self, raw_html, answer_yaml):
        with open(raw_html, 'r') as f:
            content = f.read()
        tree = html.fromstring(content)
        items = tree.xpath('//div/div[@class="cls_006"]/span | //div/div[@class="cls_010"]/span| //div/div[@class="cls_009"]/span| //div/div[@class="cls_013"]/span')
        text_list = [item.text_content() for item in items]
        section_dict = divideToSections(text_list)
        self.section_question_dict = {}
        with open(answer_yaml, 'r') as f:
            answer_dict = yaml.load(f.read())
        
        # print(section_dict['Section 51'])
        for key, content in section_dict.items():
            question_texts = divideToQuestions(section_dict[key])
            qs = [TextCompletionQuestion(key, i+1, question_texts[i], answer_dict[key][i]) for i in range(len(question_texts))]
            self.section_question_dict[key] = qs
        

class MemoryQueue():
    def __init__(self, mem_items=[]):
        self.items_que = PriorityQueue()
        for w in mem_items:
            self.items_que.put(w)
        self.head_item = None

    def HeadItem(self):
        if self.head_item is None:
            self.head_item = self.items_que.get()
        return self.head_item

    def Update(self, is_correct):
        if self.head_item is None:
            return
        self.head_item.updateTrainData(is_correct)
        self.items_que.put(self.head_item)
        self.head_item = None

    def Push(self, mem_items):
        for w in mem_items:
            self.items_que.put(w)

    def RawData(self):
        data = (w for w in self.items_que.queue)
        return data

    def __getitem__(self, i):
        for w in self.items_que.queue:
            if w.item == i:
                return w
        raise KeyError("No item: {} in lib".format(i))

class TCVis():
    CORRECT = Back.GREEN + Style.BRIGHT + 'CORRECT' + Style.RESET_ALL
    WRONG = Back.RED + Style.BRIGHT + 'WRONG' + Style.RESET_ALL

class GrediantiTextCompletionCUI():
    def __init__(self, section_ids, raw_html_folder):
        self.db_path = os.path.expanduser("~") + os.sep + ".glossary"
        self.mem_que = MemoryQueue()
        raw_html = raw_html_folder + '/gredianti_tc.html'
        answer_yaml = raw_html_folder + '/answer.yaml'
        tc_lib_full = TextCompletionLib(raw_html, answer_yaml)
        # tc_lib_list = []
        for id in section_ids:
            self.mem_que.Push(tc_lib_full.section_question_dict['Section {}'.format(id)])
        logging.info('loggin')
    
    def Close(self):
        logging.info('loggout')
    
    def RunTrain(self):
        while True:
            while True:
                start_time = time.time()
                print(TerminalVis.CLS)
                print(self.mem_que.HeadItem().__str__())
                answer = input('Select {} answer(s): '.format(len(self.mem_que.HeadItem().answer)))
                correct = False
                if answer == self.mem_que.HeadItem().answer:
                    correct = True
                    break
                elif answer == ".?": #answer
                    input(self.mem_que.HeadItem().answer)
                    break
                elif answer == ".q": #quit
                    self.Close()
                    quit()
                elif answer == "": #quit
                    continue
                else:
                    break

            while True:
                print(TerminalVis.CLS)
                print(self.mem_que.HeadItem().answerFilledStr())
                input('Answer: {}, your answer: {}, {}!'.format(self.mem_que.HeadItem().answer, answer, TCVis.CORRECT if correct else TCVis.WRONG))
                time_cost = time.time() - start_time
                logging.info("[%sQ%s] time_cost=%.3f input=%s result=%s", \
                    self.mem_que.HeadItem().section_idx, 
                    self.mem_que.HeadItem().question_idx, 
                    time_cost, answer, correct)
                try:
                    self.mem_que.Update(correct)
                except ValueError:
                    pass
                else:
                    break


class CacheManager():
    def __init__(self, cache_filename):
        self.cache_filename = cache_filename
    
    def fetchVal(self, key, example):
        tmp_dict = {}
        val = None
        if os.path.isfile(self.cache_filename):
            with open(self.cache_filename, 'r') as f:
                loaded = yaml.load(f.read())
                if loaded:
                    tmp_dict = loaded
                try:
                    val = tmp_dict[key]
                except:
                    pass
        if not val:
            print("please input {}, eg: {}".format(key, self.promp_dict[key]))
            val = input("{}: ".format(key))
            tmp_dict[key] = val
            with open(self.cache_filename, 'w') as f:
                f.write(yaml.dump(tmp_dict))
        return val

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python3 {} section_idx".format(sys.argv[0]))
        quit()

    cache = CacheManager(os.path.expanduser('~') + os.sep + '.boring_meeting')
    lang_root = cache.fetchVal("LANG_ROOT", '/home/xiache02/engineering/lang_examination_archiv_en')
    raw_html_folder =  lang_root + '/gre_exercise/gredianti/text_completion'
    gredianti_tc_log = lang_root + '/gre_exercise/gredianti/text_completion/review.log'

    section_idx = [int(idx) for idx in sys.argv[1:]]
    
    logging.basicConfig(filename=gredianti_tc_log, format='[%(asctime)s]%(message)s', level=logging.INFO)
    cui = GrediantiTextCompletionCUI(section_idx, raw_html_folder)
    cui.RunTrain()