from lxml import html
import requests
import multiprocessing as mp
from mem_word import MemWord

# page = requests.get('https://www.lexico.com/en/definition/eleemosynary')
# tree = html.fromstring(page.content)
# buyers = tree.xpath('//div[@class="senseInnerWrapper"]/p')
# print(buyers[0].text_content())

def ProcessFunc(w, q):
    mem_w = MemWord.OnlineConstruct(w)
    q.put(mem_w)

def ConcurrentInitVocabulary(words):
    q = mp.Queue()
    ps = []
    for w in words:
        p = mp.Process(target=ProcessFunc, args=(w,q))
        ps.append(p)
        p.start()

    for p in ps:
        p.join()
    voc = []
    while not q.empty():
        voc.append(q.get())
    return voc


if __name__ == "__main__":
    vocabulary = ['detection'] * 10
    voc = ConcurrentInitVocabulary(vocabulary)
    #print(q.get())
    print(voc)


