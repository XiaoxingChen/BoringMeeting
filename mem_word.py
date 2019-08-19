import sys
from colorama import Fore, Back, Style
from queue import PriorityQueue

# def LexicoWordOrigin(w):
#     from lxml import html
#     import requests

#     page = requests.get('https://www.lexico.com/en/definition/' + w)
#     tree = html.fromstring(page.content)
#     origin = tree.xpath('//div[@class="senseInnerWrapper"]/p')
#     if len(origin) == 0:
#         return ''
#     return origin[0].text_content()


class TerminalVis():
    BOLD = '\033[1m'
    CLS = '\033[H\033[J'
    @classmethod
    def Seperator(cls):
        return Fore.YELLOW + "="*50 + Style.RESET_ALL + '\n'

    @classmethod
    def MinorSeperator(cls):
        return Fore.YELLOW + "-"*10 + Style.RESET_ALL + '\n'

    @classmethod
    def MemLevel(cls):
        return Fore.RED + TerminalVis.BOLD + 'mem_level: ' + Style.RESET_ALL



class WordDefBlock():
    def __init__(self, definition, example, synonyms):
        self.definition = str(definition)
        self.example = str(example)
        self.synonyms = str(synonyms)

class POSBlock():
    def __init__(self, pos, word_defs):
        self.pos = str(pos)
        self.word_defs = word_defs

    def __str__(self):
        from colorama import Fore, Back, Style
        output = TerminalVis.Seperator()
        output += Fore.GREEN + TerminalVis.BOLD + self.pos.upper() + Style.RESET_ALL + '\n'

        for wd in self.word_defs:
            wd_buff = TerminalVis.MinorSeperator()
            wd_buff += Fore.LIGHTCYAN_EX + TerminalVis.BOLD + wd.definition + Style.RESET_ALL + Style.RESET_ALL + '\n'
            wd_buff += Fore.WHITE + wd.example + Style.RESET_ALL + '\n'
            wd_buff += Fore.LIGHTBLUE_EX + wd.synonyms + Style.RESET_ALL + '\n'
            output += wd_buff

        return output

def GetFirst(w):
    return w[0] if len(w) > 0 else ''

def LexicoWordOrigin(w):
    from lxml import html
    import requests
    page = requests.get('https://www.lexico.com/en/definition/' + w)
    # page = requests.get('http://127.0.0.1:5500/test/data/hexicon_hello.html')
    tree = html.fromstring(page.content)
    origin = GetFirst(tree.xpath('//div[@class="senseInnerWrapper"]/p'))
    origin = origin.text_content() if origin != '' else ''
    pos_block_root = tree.xpath('//section[@class="gramb"]')
    pos_blocks = []
    for pos_block in pos_block_root:
        pos = GetFirst(pos_block.xpath('h3[@class="ps pos"]/span[@class="pos"]/text()'))
        meaning_block = pos_block.xpath('ul[@class="semb"]/li/div[@class="trg"]')
        word_def_blocks = []
        for m in meaning_block:
            meaning = GetFirst(m.xpath('p/span[@class="ind"]/text()'))
            #print("meaning: {}".format(meaning))
            example = GetFirst(m.xpath('div[@class="exg"]/div[@class="ex"]/em/text()'))
            synonyms = GetFirst(m.xpath('div[@class="synonyms"]/div[@class="exg"]/div'))
            synonyms = synonyms.text_content() if synonyms != '' else ''
            word_def_blocks.append(WordDefBlock(meaning, example, synonyms))
        pos_blocks.append(POSBlock(pos, word_def_blocks))

    derivative_word = GetFirst(tree.xpath('//section[@class="gramb"]/div[@class="empty_sense"]/p[@class="derivative_of"]/a/text()'))
    derivative_of = MemWord.OnlineConstruct(derivative_word) if derivative_word != '' else None
    return pos_blocks, origin, derivative_of

    # if len(origin) == 0:
    #     return ''
    # return origin[0].text_content()

class MemWord():
    def __init__(self, word, mem_level, pos_blocks, origin, dervative_of=None):
        self.word = word
        self.mem_level = mem_level
        self.pos_blocks = pos_blocks
        self.definition_cn = ''
        self.origin = str(origin)
        self.dervative_of = dervative_of

    @property
    def vis_word(cls):
        return Fore.LIGHTGREEN_EX + TerminalVis.BOLD + cls.word + Style.RESET_ALL

    def __str__(self):
        if self.dervative_of is not None:
            result = Fore.RED + TerminalVis.BOLD + 'DEFINITION EMPTY: ' + Style.RESET_ALL
            result += '"{}" is the derivative of "{}"\n'.format(self.word, self.dervative_of.word)
            return result + self.dervative_of.__str__()

        result = ""
        for b in self.pos_blocks:
            result += b.__str__()
        result += TerminalVis.Seperator()
        result += self.origin + '\n'
        return result

    def __lt__(self, other):
        return self.mem_level > other.mem_level

    def Vague(self):
        self.mem_level += 0.05

    @classmethod
    def OnlineConstruct(cls, word):
        pos_blocks, origin, derivative_of = LexicoWordOrigin(word)
        return cls(word, 3.,pos_blocks, origin, derivative_of)

class MemVocabulary():
    def __init__(self, mem_words=[]):
        self.words_que = PriorityQueue()
        for w in mem_words:
            self.words_que.put(w)
        self.head_word = None

    def HeadWord(self):
        if self.head_word is None:
            self.head_word = self.words_que.get()
        return self.head_word

    def Update(self, mem_level_top):
        if self.head_word is None:
            return
        for w in self.words_que.queue:
            w.Vague()
        self.head_word.mem_level = mem_level_top
        self.words_que.put(self.head_word)
        self.head_word = None

    def Push(self, mem_words):
        for w in mem_words:
            self.words_que.put(w)

    def __getitem__(self, i):
        for w in self.words_que.queue:
            if w.word == i:
                return w
        raise KeyError("No word: {} in vocabulary".format(i))




if __name__ == "__main__":
    import yaml
    wdb = WordDefBlock("a", "b", "c")
    print(vars(wdb))

    pbs = []
    pbs.append(POSBlock("haha", [wdb]))
    pbs.append(POSBlock("ddd", [wdb]))
    serialized = yaml.dump(pbs)
    print(serialized)
    pb2 = yaml.load(serialized)
    print(pb2)