class MyObject():
    def __init__(self):
        self.un = 1
        self.deux = 2
        self.trois = 3
    def __repr__(self):
        return "{}, {}, {}".format(self.un, self.deux, self.trois)
    def __str__(self):
        return "un: {}\ndeux: {}\ntrois: {}".format(self.un, self.deux, self.trois)