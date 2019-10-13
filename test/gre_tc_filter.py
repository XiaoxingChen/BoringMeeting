#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'test'))
	print(os.getcwd())
except:
	pass

from lxml import html
import re

class Options(object):
    def __init__(self, option_texts):
        self.blank_num = 1
        self.option_dict = {}
        if 12 == len(option_texts):
            option_texts = option_texts[3:]
            self.blank_num = 3
        elif 8 == len(option_texts):
            option_texts = option_texts[2:]
            self.blank_num = 2
        for text in option_texts:
            key, val = text.split('. ')
            self.option_dict[key] = val

    def __str__(self):
        if 1 == self.blank_num:
            result = '\n'.join(["{}. {}".format(key, self.option_dict[key]) for key in sorted(self.option_dict)])
        elif 2 == self.blank_num:
            result = \
'''
A. {}\t\tD. {}
B. {}\t\tE. {}
C. {}\t\tF. {}
'''.format(
                self.option_dict['A'], 
                self.option_dict['D'],
                self.option_dict['B'],
                self.option_dict['E'],
                self.option_dict['C'],
                self.option_dict['F'])
        elif 3 == self.blank_num:
            result = \
'''
A. {}\t\tD. {}\t\tG. {}
B. {}\t\tE. {}\t\tH. {}
C. {}\t\tF. {}\t\tI. {}
'''.format(
                self.option_dict['A'], 
                self.option_dict['D'],
                self.option_dict['G'],
                self.option_dict['B'],
                self.option_dict['E'],
                self.option_dict['H'],
                self.option_dict['C'],
                self.option_dict['F'],
                self.option_dict['I'])
        return result

class TextCompletionQuestion(object):
    def __init__(self, section_idx, raw_text):
        divide_idx = None
        for i in range(len(raw_text)):
            if re.fullmatch('A\.\s.*', raw_text[i]) or re.fullmatch('Blank \(i\)', raw_text[i]):
                divide_idx = i
                break
        self.question_text = ' '.join([t for t in raw_text[:divide_idx]])
        self.options = Options(raw_text[divide_idx:])
        self.section_idx = section_idx
        self.answer = 'ABC'[:self.options.blank_num]

    def __str__(self):
        result = self.question_text + '\n'*2
        result += self.options.__str__()
        return result

    def answerFilledStr(self):
        result = self.__str__()
        if 1 == self.options.blank_num:
            target_str = '/'.join([self.options.option_dict[c] for c in self.answer])
            target_str = '\033[4m' + target_str + '\033[0m'
            result = result.replace('_____', target_str)
        else : # blank > 1
            target_strings = ['\033[4m' + self.options.option_dict[c] + '\033[0m' for c in self.answer]
            for i in range(self.options.blank_num):
                result = result.replace('({})_____'.format('i'*(i+1)), target_strings[i])
        return result

def divideToSections(texts):
    texts_by_section = {}
    last_anchor_idx = 0
    for i in range(len(texts)):
        if not re.fullmatch('Section\s(\d{1,2})', texts[i]):
            continue
        if last_anchor_idx > 0:
            texts_by_section[texts[last_anchor_idx]] = texts[last_anchor_idx + 1: i]
        last_anchor_idx = i
    texts_by_section[texts[last_anchor_idx]] = texts[last_anchor_idx + 1:]
    return texts_by_section

def divideToQuestions(texts_in_section):
    tc_questions = []
    last_idx = 0
    for i in range(len(texts_in_section)):
        if not re.fullmatch('\d{1,2}\.\s.*', texts_in_section[i]):
            continue
        if 0 == i:
            continue
        tc_questions.append(texts_in_section[last_idx: i])
        last_idx = i
    tc_questions.append(texts_in_section[last_idx:])
    return tc_questions


#%%
if __name__ == "__main__":
    input_file = "/home/chenxx/engineering/lang_examination_archiv_en/gre_exercise/gredianti/text_completion/gredianti_tc.html"
    with open(input_file, 'r') as f:
        content = f.read()
    tree = html.fromstring(content)
#%%
    items = tree.xpath('//div/div[@class="cls_006"]/span | //div/div[@class="cls_010"]/span| //div/div[@class="cls_009"]/span')
    # for i in range(0,100):
    #     print(item[i].text_content())
    texts = [item.text_content() for item in items]
#%%
    section_dict = divideToSections(texts[:350])

    # print(section_dict['Section 3'])
    qs = [TextCompletionQuestion('Section 3',raw_text) for raw_text in divideToQuestions(section_dict['Section 3'])]

    for q in qs:
        print(q.answerFilledStr())
    # print(qs[1])
    # print(qs[0].options)

#%%
