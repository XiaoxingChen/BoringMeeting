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
    doc = requests.get('https://lex-audio.useremarkable.com/mp3/capriciousness_gb_1.mp3')
    with open("word.mp3", 'wb') as f:
        f.write(doc.content)


#%%
