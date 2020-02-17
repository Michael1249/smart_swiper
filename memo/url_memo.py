import json
import os
 
class Memo:
    def __init__(self):
        folder = os.path.dirname(os.path.abspath(__file__))

        self.memo = {}
        self.file_name = folder + '/url_memo.json'
        self.load_memo()
        try:
            with open(folder + '/url_memo_backup.json', 'w') as file:
                json.dump(self.memo, file, indent=4, sort_keys=True)
        except:
            pass
    
    def getURLs(self):
        return self.memo.keys()

    def load_memo(self):
        try:
            if (self.memo == {}):
                with open(self.file_name, 'r') as file:
                    self.memo = json.load(file)
        except:
            pass

    def add_urls(self, urls):
        for key in urls:
            if not urls[key]:
                if key in self.memo:
                    urls[key] = self.memo[key]

        self.memo.update(urls)

        with open(self.file_name, 'w') as file:
            json.dump(self.memo, file, indent=4, sort_keys=True)

memo = Memo()