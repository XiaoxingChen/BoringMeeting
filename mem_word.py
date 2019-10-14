import sys
from colorama import Fore, Back, Style
from queue import PriorityQueue


def GetFirst(w, empty=''):
    return w[0] if len(w) > 0 else empty

class TerminalVis():
    # BOLD = '\033[1m'
    CLS = '\033[H\033[J'
    
    @classmethod
    def VerticalSpacing(cls, h=10):
        return '\n'*h

    @classmethod
    def Seperator(cls):
        return Fore.YELLOW + "="*50 + Style.RESET_ALL + '\n'

    @classmethod
    def MinorSeperator(cls):
        return Fore.YELLOW + "-"*10 + Style.RESET_ALL + '\n'

    @classmethod
    def MemLevel(cls):
        return Fore.RED + Style.BRIGHT + 'mem_level: ' + Style.RESET_ALL

class WordDefBlock():
    def __init__(self, definition, example, synonyms):
        self.definition = str(definition)
        self.example = str(example)
        self.synonyms = str(synonyms)

    # @classmethod
    # def FromLxmlNode(cls, meaning_block):
    #     meaning = GetFirst(meaning_block.xpath('p/span[@class="ind"]/text()'))
    #     example = GetFirst(meaning_block.xpath('div[@class="exg"]/div[@class="ex"]/em/text()'))
    #     synonyms = GetFirst(meaning_block.xpath('div[@class="synonyms"]/div[@class="exg"]/div'))
    #     synonyms = synonyms.text_content() if synonyms != '' else ''
    #     return cls(meaning, example,synonyms)

class POSBlock():
    def __init__(self, pos, word_defs):
        self.pos = str(pos)
        self.word_defs = word_defs

    def __str__(self):
        from colorama import Fore, Back, Style
        output = TerminalVis.Seperator()
        output += Fore.GREEN + Style.BRIGHT + self.pos.upper() + Style.RESET_ALL + '\n'

        for wd in self.word_defs:
            wd_buff = TerminalVis.MinorSeperator()
            wd_buff += Fore.LIGHTCYAN_EX + Style.BRIGHT + wd.definition + Style.RESET_ALL + Style.RESET_ALL + '\n'
            wd_buff += Fore.WHITE + wd.example + Style.RESET_ALL + '\n'
            wd_buff += Fore.LIGHTBLUE_EX + wd.synonyms + Style.RESET_ALL + '\n'
            output += wd_buff

        return output


def LexiconWordPage(w):
    from lxml import html
    import requests
    page = requests.get('https://www.lexico.com/en/definition/' + w)
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
            example = GetFirst(m.xpath('div[@class="exg"]/div[@class="ex"]/em/text()'))
            synonyms = GetFirst(m.xpath('div[@class="synonyms"]/div[@class="exg"]/div'))
            synonyms = synonyms.text_content() if synonyms != '' else ''
            word_def_blocks.append(WordDefBlock(meaning, example, synonyms))
        pos_blocks.append(POSBlock(pos, word_def_blocks))

    derivative_word = GetFirst(tree.xpath('//section[@class="gramb"]/div[@class="empty_sense"]/p[@class="derivative_of"]/a/text()'), empty=None)
    deriv_of = HyperTextMemWord.OnlineConstruct(derivative_word).mem_word if derivative_word is not None else None

    pron_root = GetFirst(tree.xpath('//section[@class="pronSection etym"]/div[@class="pron"]'), empty=None)

    mem_word = MemWord(w, pos_blocks, origin, derivative_of=deriv_of)
    hyper_text_mem_word = HyperTextMemWord(mem_word)
    if pron_root is not None:
        audio_link = GetFirst(pron_root.xpath('a[@class="speaker"]/audio/@src'), empty=None)
        print(audio_link)
        hyper_text_mem_word.mem_word.phoneticspelling = GetFirst(pron_root.xpath('span[@class="phoneticspelling"]/text()'))
        hyper_text_mem_word.audio = requests.get(audio_link).content if audio_link is not None else None
    return hyper_text_mem_word

class MemWord():
    vague_step = 0.05
    def __init__(self, word, pos_blocks=[], origin='', phoneticspelling='', derivative_of=None):
        self.word = word
        self.mem_level = 3.
        self.pos_blocks = pos_blocks
        self.definition_cn = ''
        self.origin = str(origin)
        self.derivative_of = derivative_of
        self.phoneticspelling = phoneticspelling

    @property
    def vis_word(cls):
        return Fore.LIGHTGREEN_EX + Style.BRIGHT + cls.word + Style.RESET_ALL

    def __str__(self):
        if self.derivative_of is not None:
            result = Fore.RED + Style.BRIGHT + 'DEFINITION EMPTY: ' + Style.RESET_ALL
            result += '"{}" is the derivative of "{}"\n'.format(self.word, self.derivative_of.word)
            return result + self.derivative_of.__str__()

        result = self.vis_word + ": " + self.phoneticspelling + '\n'
        for b in self.pos_blocks:
            result += b.__str__()
        result += TerminalVis.Seperator()
        result += Fore.GREEN + Style.BRIGHT + 'ORIGIN: ' + Style.RESET_ALL + '\n'
        result += self.origin + '\n'
        return result

    def VisMaskedString(self):
        import re
        result = self.__str__()
        result = re.sub(r"^(.*?" + self.word + r".*?):\s/(.*?)/\n", r'\1: _________\n', result)
        result = re.sub(self.word, '_'*len(self.word), result, flags=re.IGNORECASE)
        result = re.sub(r"\n.*?ORIGIN:[\s\S]*?$", '\n', result)
        return result

    def __lt__(self, other):
        return self.mem_level > other.mem_level

    def Vague(self):
        self.mem_level += MemWord.vague_step

class HyperTextMemWord(object):
    def __init__(self, mem_word, audio=None):
        self.mem_word = mem_word
        self.audio = audio

    @classmethod
    def OnlineConstruct(cls, word):
        return LexiconWordPage(word)

class MemWordQueue():
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
        self.head_word.mem_level += (mem_level_top - 3.)
        self.words_que.put(self.head_word)
        self.head_word = None

    def Push(self, mem_words):
        for w in mem_words:
            self.words_que.put(w)

    def RawData(self):
        data = (w for w in self.words_que.queue)
        return data

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