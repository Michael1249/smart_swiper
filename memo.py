import json


class FileObserver:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, 'r+')


class DataSnapshot:
    def __init__(self, entries={}):
        self.__dict__.update(entries)

    def json(self):
        return self.__dict__

    def update(self, json):
        self.__dict__.update(json)
        return self

    def filter(self, predicate):
        result = DataSnapshot()
        for key, value in self.json().items():
            if predicate(key, value):
                result.update({key: value})
        return result

    def transform(self, mask):
        print(mask)

        def transformPair(key, value, mask):
            if mask == any:
                return {key: value}
            elif callable(mask):
                return mask(key, value)
            else
                return {key: transformJson(value, mask)}

        def transformValue(value, mask):
            if mask == any:
                return {key: value}
            elif callable(mask):
                return mask(key, value)
            else
                return {key: transformJson(value, mask)}

        def transformList(listVal, mask):
            result = []

            for val, maskVal in zip(listVal, mask):
                result.append(transformValue(val, maskVal))
            
            return result

        def transformDict(dictVal, mask):
            result = {}

            for key, mask in mask.items():
                result.update(transformPair(key, dictVal[key], mask))
            
            return result

        def transformJson(json, mask):
            if type(json) is list:
                return transformList(json, mask)
            elif type(json) is dict:
                return transformDict(json, mask)
            else:
                pass

        return DataSnapshot()


class Memo(FileObserver):
    def __init__(self, file_path):
        super(Memo, self).__init__(file_path)
        self.data = DataSnapshot()
        self.sync()

    def sync(self):
        self.data = DataSnapshot(json.load(self.file))

    def save(self):
        self.file.seek(0)
        json.dump(self.data.json(), self.file, indent=4, sort_keys=True)
        self.file.truncate()


memo = Memo('C:/my/test.json')
memo.save()
print(memo.data.transform({'a': any, 'b': {'d': }}).json())
