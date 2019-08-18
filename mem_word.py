import sys
from colorama import Fore, Back, Style

def LexicoWordOrigin(w):
    from lxml import html
    import requests

    page = requests.get('https://www.lexico.com/en/definition/' + w)
    tree = html.fromstring(page.content)
    origin = tree.xpath('//div[@class="senseInnerWrapper"]/p')
    if len(origin) == 0:
        return ''
    return origin[0].text_content()

def GoogleTransMeaning(translator, w):
    result = translator.translate(w, dest='zh-cn')

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
        self.definition = definition
        self.example = example
        self.synonyms = synonyms

class POSBlock():
    def __init__(self, pos, word_defs):
        self.pos = pos
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
    tree = html.fromstring(page.content)
    origin = GetFirst(tree.xpath('//div[@class="senseInnerWrapper"]/p'))
    origin = origin.text_content() if origin != '' else ''
    pos_block_root = tree.xpath('//section[@class="gramb"]')
    pos_blocks = []
    for pos_block in pos_block_root:
        pos = pos_block.xpath('h3[@class="ps pos"]/span[@class="pos"]/text()')[0]
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

    derivative_word = GetFirst(tree.xpath('//div[@class="empty_sense"]/p[@class="derivative_of"]/a/text()'))
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
        self.origin = origin
        self.dervative_of = dervative_of
        self.vis_word = Fore.LIGHTGREEN_EX + TerminalVis.BOLD + word + Style.RESET_ALL

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

    @classmethod
    def OnlineConstruct(cls, word):
        pos_blocks, origin, derivative_of = LexicoWordOrigin(word)
        return cls(word, 3.,pos_blocks, origin, derivative_of)

    @staticmethod
    def Vocabulary(words):
        voc = []
        for w in words:
            voc.append(MemWord.OnlineConstruct(w))
        return voc

if __name__ == "__main__":
    print("dict")