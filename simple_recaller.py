import sys
from html_to_momo import ExtractWordsFromHtmlVocabulary
import os
import glob
from gredianti_tc_cui import CacheManager
#from googletrans import Translator


def MemLevel(cls):
        return cls.mem_level

def UpdateMemWords(mem_words):
    for w in mem_words:
        w.mem_level += 0.1
    mem_words.sort(key=MemLevel , reverse=True)

if __name__ == "__main__":
    from vocabulary_cui import VocabularyCUI
    from mem_word import TerminalVis
    if len(sys.argv) < 2:
        print("eg.: python {} vocabulary.html".format(sys.argv[0]))
        quit()
    
    html_files = sys.argv[1:]
    
    # print(os.curdir)
    # work_folder = os.path.abspath(os.path.dirname(html_files[0]))
    cache = CacheManager(os.path.expanduser('~') + os.sep + '.boring_meeting')
    lang_root = cache.fetchVal("LANG_ROOT", '/home/xiache02/engineering/lang_examination_archiv_en')

    
    words = []
    for html_filename in html_files:
        words += ExtractWordsFromHtmlVocabulary(html_filename)
    cui = VocabularyCUI(words, lang_root)

    try:
        cui.RunSpell()
    except KeyboardInterrupt:
        cui.Close()
        quit()

