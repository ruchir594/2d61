class User(object):
    def __init__(self):
        self.users = [['30001', 'qwerty30'], ['10002', 'qwerty2'], ['10003', 'qwerty3'], ['70007', 'qwerty7']]
        self.d = {}
        self.d['30001'] = 'editor'
        self.d['10002'] = 'author'
        self.d['10003'] = 'author'
        self.d['70007'] = 'reviewer'

    def find(self, strx):
        return self.d[strx]
