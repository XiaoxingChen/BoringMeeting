import sys
from gredianti_tc_cui import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python3 {} section_idx".format(sys.argv[0]))
        quit()

    section_idx = sys.argv[1]

    cache = CacheManager(os.path.expanduser('~') + os.sep + '.boring_meeting')
    lang_root = cache.fetchVal("LANG_ROOT", '/home/xiache02/engineering/lang_examination_archiv_en')
    raw_html_folder =  lang_root + '/gre_exercise/gredianti/text_completion'

    raw_html = raw_html_folder + '/gredianti_tc.html'
    answer_yaml = raw_html_folder + '/answer.yaml'
    tc_lib_full = TextCompletionLib(raw_html, answer_yaml)

    section_dict = tc_lib_full.section_question_dict['Section {}'.format(section_idx)]
    for q in section_dict:
        print(q.answerFilledStr(), end='\n\n')