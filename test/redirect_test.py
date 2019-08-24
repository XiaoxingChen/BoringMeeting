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
    headers = {
        'Host': 'www.lexico.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'ahoy_visitor=2a6581e7-a3c6-4a24-a7de-66260104b10c; _ga=GA1.2.1769632778.1565699548; __gads=ID=0a71bfa419751d28:T=1565699550:S=ALNI_MZ0IzQkxHdGdY2ObNVEF0cBCyZzsQ; __qca=P0-242402283-1565699552141; cto_lwid=4a367726-246a-4d90-911e-b1bc2e26894b; request_method=GET; _lexico_remarkable_session=cnVVMFZRMGFKcUZHV3o2enllY2JwRElsQkZjTTVpVmU4cjhKY2Y4ZTFYMHIxMWhOODVtMTJEZGE3bDZ6Nm9TOG1HUjRrbnpsUXB2SExVeUpTWW9EMjYzaUM3Z1UrR002Zk9mL0RPOTlmSXlZeld0SjgydGpRRmtTS3FQbFNRM3dQL1pQSGg4anFQZWhEYW5qTHhQdHhJMUlKU21SWmZFNWZYNDhiZzgvZWk5dTc5Z2k4eFZZc2FhUVBaM0VqUC9tOXNyZDlNR21Bc3pOWXlQeWQxTmFzYlBKY1BlMDZ5N2JZeVpVZmlLa0ljMTFWVkg0eWZ5a1FLOVJvNVJFOVp6SmxQOTNsTWFaWFYwcFlRbTJ0MzljdnZUeVU0TWNXN1Q3NXNhSFk5SGRRT2FpM2p6M0lPWW4xbUYwQUVNb2Jqc0c0KzhGTkNzRVpnYjlYbzRnR2ZaTVZEVmMzeGh2OUh6WXpiOGppbUhzZHhzeS94MUVHL09tNjA1dkMybmFFTklhNGg1dnRlZnFhdW8vZ2t6bUZUaXh0Zz09LS0xWUJtOWZSbWhmWXp0OVFIK2hwS01BPT0%3D--9dcf55071de444817782fbd1e3d62e7cc8bce056; cto_idcpy=a12de11b-fc1c-4aa2-9268-74e18dcf9dfb; cto_bundle=FMBhuV9OM04zSlVPb2ZlSTk0UEY4SnM3SXJmM1NSY1dQdklRR3Y4S0h0NTBHNlolMkJjRXV1SGVXY3ZoZGg3U1BFUDZyb3YlMkJUMzhOcnpmNmFhMnFwVDZlOENMcmFYSU42Smx0elpYU3FLbkhmZ1dpR1VaeHNJMm1BbHZVQkFqOUsxZm5GekpxUDR4ZSUyQlpQeFhHJTJCNmtXJTJCOUpvYjRBJTNEJTNE; ahoy_visit=82a6a5ee-0afe-4ac9-a9ab-f55cf5399750; _gid=GA1.2.63138275.1566568779',
        'Upgrade-Insecure-Requests': 1,
        'TE': 'Trailers'}
    response = requests.get('https://www.lexico.com/en/search?filter=dictionary&query=revelations', headers=headers)

#%%
    print(response.status_code)
    # print(response.history.)
    for p in response.history:
        print(p.url)
    # print(response.headers)
    print(response.headers['localtion'])
    # print(response.url)
    # print(page.url)
    # if page.history:
    #     print(page.url)
    #     page = requests.get(page.url)



#%%
