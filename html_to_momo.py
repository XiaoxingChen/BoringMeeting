import re
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

def ExtractWordsFromHtmlVocabulary(html_filename):
    html_file = open(html_filename, 'r')
    html_str = html_file.read()
    vocabulary_table = ExtractVocabularyTable(html_str)
    words = ExtractHtmlTableFirstColumn(vocabulary_table)
    return words


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("eg.: python {} vocabulary.html".format(sys.argv[0]))
        quit()

    html_filename = sys.argv[1]
    # html_file = open(html_filename, 'r')
    # html_str = html_file.read()
    # vocabulary_table = ExtractVocabularyTable(html_str)
    # words = ExtractHtmlTableFirstColumn(vocabulary_table)
    words = ExtractWordsFromHtmlVocabulary(html_filename)
    print("totally {} words".format(len(words)))
    for w in words:
        print(w)
    # print(words)
