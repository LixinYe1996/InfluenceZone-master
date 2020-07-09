class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "Point #{}: ({}, {})".format(self.id, self.x, self.y)


# 分割
class Segment:
    def __init__(self, spoint, epoint):
        self.spoint = spoint
        self.epoint = epoint

    def __str__(self):
        return "Segment #({}, {})".format(self.spoint, self.epoint)


# 线
class Line:
    def __init__(self, m, c):
        self.m = m
        self.c = c

    def __str__(self):
        return "Line #({}, {})".format(self.m, self.c)
