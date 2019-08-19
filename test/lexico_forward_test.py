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
    # page = requests.get('https://www.lexico.com/en/definition/course')
    page = requests.get('https://www.lexico.com/en/definition/capriciousness')



#%%

tree = html.fromstring(page.content)
#     meaning_block = tree.xpath('//section[@class="gramb"]/ul[@class="semb"]/li/div[@class="trg"]/p/span[@class="ind"]')
pos_block_root = tree.xpath('//section[@class="gramb"]')[0]
print(len(pos_block_root))
pos = pos_block_root.xpath('h3[@class="ps pos"]/span[@class="pos"]/text()')
print(pos[0])
derive_of = tree.xpath('//section[@class="gramb"]/div[@class="empty_sense"]/p[@class="derivative_of"]/a')
# derive_of = tree.xpath('//div[@class="empty_sense"]/p[@class="derivative_of"]/a')

print(derive_of[0].text_content())


