import readline
from queue import PriorityQueue
import yaml
from test.gre_tc_filter import *
from lxml import html
import re
from mem_word import TerminalVis

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
            qs = [TextCompletionQuestion(key, raw_text) for raw_text in divideToQuestions(section_dict[key])]
            for i in range(len(qs)):
                # print("sec: {}, q: {}".format(key, qs[i]))
                qs[i].answer = answer_dict[key][i]
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
    
    def Close(self):
        pass
    
    def RunTrain(self):
        while True:
            while True:
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
                else:
                    break

            while True:
                print(TerminalVis.CLS)
                print(self.mem_que.HeadItem().answerFilledStr())
                input('Answer: {}, your answer: {}, {}!'.format(self.mem_que.HeadItem().answer, answer, 'RIGHT' if correct else 'WRONG'))
                try:
                    self.mem_que.Update(correct)
                except ValueError:
                    pass
                else:
                    break

if __name__ == "__main__":
    
    
    raw_html_folder = '/home/chenxx/engineering/lang_examination_archiv_en/gre_exercise/gredianti/text_completion'
    cui = GrediantiTextCompletionCUI([10], raw_html_folder)
    cui.RunTrain()