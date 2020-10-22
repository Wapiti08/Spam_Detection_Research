# 

import requests

def cloaked_links():
    response = requests.get(someurl)
    if response.history:
        print("Request was redirected")
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    else:
        print("Request was not redirected")
    
    


    pass

def redirected_links():
    pass