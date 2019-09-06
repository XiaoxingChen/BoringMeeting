import re
import os
import glob
import sys

def ExtractVocabularyTable(text_file):
    pattern = 'vocabulary.*\n\s*<table>((.|\n)*?)</table>'
    match_list = re.findall(pattern, text_file, flags=re.MULTILINE)
    if len(match_list) == 0:
        raise ValueError("no vocabulary segment found!")
    return match_list[0][0]

def ExtractHtmlTableFirstColumn(text_file):
    pattern = '<tr>(.|\n)*?<td>(.*?)</td>'
    match_list = re.findall(pattern, text_file, flags=re.MULTILINE)
    words = [m[1] for m in match_list]
    return words

def NoPhrase(items):
    words = []
    for i in items:
        if ' ' in i:
            continue
        if len(i) == 0:
            continue
        words.append(i)
    return words

def ExtractWordsFromHtmlVocabulary(html_filename):
    html_file = open(html_filename, 'r')
    html_str = html_file.read()
    try:
        vocabulary_table = ExtractVocabularyTable(html_str)
    except ValueError:
        raise ValueError("no vocabulary segment found in {}".format(html_filename))
    items = ExtractHtmlTableFirstColumn(vocabulary_table)
    return NoPhrase(items)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("eg.: python {} vocabulary.html".format(sys.argv[0]))
        quit()

    input_path = sys.argv[1]
    
    if os.path.isfile(input_path):
        html_filename = input_path
        words = ExtractWordsFromHtmlVocabulary(html_filename)
        # cui = VocabularyCUI(words, os.path.dirname(html_filename))
    elif os.path.isdir(input_path):
        work_folder = input_path
        html_files = glob.glob(work_folder + os.sep + "section_**.html")
        words = []
        for html_filename in html_files:
            words += ExtractWordsFromHtmlVocabulary(html_filename)
        # cui = VocabularyCUI(words, work_folder)
    else:
        raise ValueError("invalid input param")

    # words = ExtractWordsFromHtmlVocabulary(html_filename)


    print("totally {} words".format(len(words)))
    for w in words:
        print(w)
    # print(words)
