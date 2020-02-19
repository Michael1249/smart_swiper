import json
import os
from datetime import date
from utils import timeshtamp


class Memo:
    def __init__(self):
        folder = os.path.dirname(os.path.abspath(__file__))

        self.memo = {}
        self.file_name = folder + '/url_memo.json'
        self.load_memo()

        if not os.path.isdir(folder + '/backup/'):
            os.mkdir(folder + '/backup/') 
        try:
            with open(folder + '/backup/' + timeshtamp() + '_url_memo_backup.json', 'w') as file:
                json.dump(self.memo, file, indent=4, sort_keys=True)
        except:
            pass
    
    def getURLs(self):
        return list(self.memo.keys())
    
    def getUrlData(self, url):
        return self.memo[url]

    def load_memo(self):
        try:
            if (self.memo == {}):
                with open(self.file_name, 'r') as file:
                    self.memo = json.load(file)
        except:
            pass

    def save_urls(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.memo, file, indent=4, sort_keys=True)

    def upd_urls(self, urls):
        def merge(source, destination):
            for key, value in source.items():
                if isinstance(value, dict):
                    # get node or create one
                    node = destination.setdefault(key, {})
                    merge(value, node)
                else:
                    destination[key] = value

            return destination
        self.memo = merge(urls, self.memo)
        self.save_urls()

    def remove_urls(self, urls):
        for url in urls:
            del self.memo[url]
        
        self.save_urls()

    def get_fields(self, field):
        return [x[field] for x in self.memo.values()]

    def size(self):
        return len(self.memo)


memo = Memo()
