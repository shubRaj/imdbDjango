#! /usr/bin/env python3
import requests
import json
import re
class ImdbApi:
    def __init__(self,search):
        self._search = str(search).lower()
        self._response = requests.get("https://sg.media-imdb.com/suggests/%s/%s"%(self._search[0],self._search.replace(' ','+'))+".json").content
        self._cvtAble = lambda response,search:response.decode("utf-8").lstrip("imdb$%s("%search.replace(' ','_')).rstrip(")")
    def json(self):
        data = json.loads(self._cvtAble(self._response,self._search))
        data = data.get("d",None)
        if data is not None:
            return data
        return {}
    def num_items(self):
        return len(self.json())
    def ids(self):
        regex = re.compile("\d+")
        data = [regex.search(item.get("id",None)).group() for item in self.json()]
        return data
if __name__=="__main__":
    print(ImdbApi("matrix").ids())