import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __eq__(self, other):
        '''重写equal函数'''
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str((self.x, self.y))

    def move(self, d):
        return (self.x+d[0], self.y+d[1])


if __name__ == "__main__":
    p1 = Point(1,2)
    p2 = Point(2,3)
    print((p1+p2))
    print((p1.move((1,1))))
    print(Point(1,2) in [p1,p2])