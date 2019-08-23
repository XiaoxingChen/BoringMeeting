#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'test'))
	print(os.getcwd())
except:
	pass
#%%
from lxml import html
import requests

if __name__ == "__main__":
    from lxml import html
    import requests

    page = requests.get('https://www.lexico.com/en/definition/revelation')
#%%
    tree = html.fromstring(page.content)
    pron_root = tree.xpath('//section[@class="pronSection etym"]/div[@class="pron"]')[0]

#%%
    # print(pron_root.xpath('span[@class=phoneticspelling]'))
    phonetic_spelling = pron_root.xpath('span[@class="phoneticspelling"]/text()')
    print(phonetic_spelling)


#%%
    audio_link = pron_root.xpath('a[@class="speaker"]/audio/@src')
    print(audio_link[0])

    doc = requests.get(audio_link[0])
    with open("word.mp3", 'wb') as f:
        f.write(doc.content)


#%%
