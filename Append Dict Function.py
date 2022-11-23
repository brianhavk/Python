class myDict(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        if self.get(key)!=None:
            print('key', key, 'already used')
        self.setdefault(key, value) 


## example

myd = myDict()
name = "fred"

myd.add('apples',6)
print('\n', myd)
myd.add('bananas',3)
print('\n', myd)
myd.add('jack', 7)
print('\n', myd)
myd.add(name, myd)
print('\n', myd)
myd.add('apples', 23)
print('\n', myd)
myd.add(name, 2)
print(myd)