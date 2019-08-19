import sys
from html_to_momo import ExtractWordsFromHtmlVocabulary
import os
import glob
#from googletrans import Translator


def MemLevel(cls):
        return cls.mem_level

def UpdateMemWords(mem_words):
    for w in mem_words:
        w.mem_level += 0.1
    mem_words.sort(key=MemLevel , reverse=True)

if __name__ == "__main__":
    from vocabulary_trainer import VocabularyTrainer
    from mem_word import TerminalVis
    if len(sys.argv) < 2:
        print("eg.: python {} vocabulary.html".format(sys.argv[0]))
        quit()

    input_path = sys.argv[1]
    trainer = None
    if os.path.isfile(input_path):
        html_filename = input_path
        words = ExtractWordsFromHtmlVocabulary(html_filename)
        trainer = VocabularyTrainer(words, os.path.dirname(html_filename))
    elif os.path.isdir(input_path):
        work_folder = input_path
        html_files = glob.glob(work_folder + os.sep + "section_**.html")
        words = []
        for html_filename in html_files:
            words += ExtractWordsFromHtmlVocabulary(html_filename)
        trainer = VocabularyTrainer(words, work_folder)
    else:
        raise ValueError("invalid input param")

    trainer.Run()

if __name__ == "__main2__":
    from mem_vocabulary import ConcurrentInitVocabulary
    from mem_word import TerminalVis
    if len(sys.argv) < 2:
        print("eg.: python {} vocabulary.html".format(sys.argv[0]))
        quit()
    html_filename = sys.argv[1]
    words = ExtractWordsFromHtmlVocabulary(html_filename)
    mem_words = ConcurrentInitVocabulary(words)
    #mem_words = LoadMemWords(words)
    while True:
        UpdateMemWords(mem_words)
        input((mem_words[0].vis_word).center(100))
        print(mem_words[0])
        while True:
            try:
                level = input(TerminalVis.MemLevel())
                print(TerminalVis.CLS)
                print('\n' * 10)
                mem_words[0].mem_level = float(level)
            except ValueError:
                pass
            else:
                break
