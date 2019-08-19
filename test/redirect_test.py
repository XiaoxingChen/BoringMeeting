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
    response = requests.get('https://www.lexico.com/en/definition/revelations')
    if response.history:
        print("Request was redirected")
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    else:
        print("Request was not redirected")
    page = response
    # print(page.url)
    # if page.history:
    #     print(page.url)
    #     page = requests.get(page.url)


#%%
    tree = html.fromstring(page.content)
#     meaning_block = tree.xpath('//section[@class="gramb"]/ul[@class="semb"]/li/div[@class="trg"]/p/span[@class="ind"]')
    pos_block_root = tree.xpath('//section[@class="gramb"]')[0]
    print(len(pos_block_root))
    pos = pos_block_root.xpath('h3[@class="ps pos"]/span[@class="pos"]/text()')
    print(pos[0])


#%%
