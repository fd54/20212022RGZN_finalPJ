import sys
from random import randint
class Map:
    def __init__(self, mapsize, mode="random", s=(1,1), g=None, blocksize=10):

        self.mapsize = mapsize
        self.blocksize = blocksize
        self.s = s
        if g:
            self.g = g
        else:
            self.g = (mapsize[0]-1, mapsize[1]-1)
        self.obs = self.generate_obstacle()
        if mode == "random":
            self.random_generate()

    def generate_obstacle(self):
        obs = []
        m, n = self.mapsize[0], self.mapsize[1]
        for i in range(m):
            if (i,0) not in obs:
                obs.append((i,0))
            if (i,n-1) not in obs:
                obs.append((i,n-1))
        for i in range(n):
            if (0,i) not in obs:
                obs.append((0,i))
            if (n-1,i) not in obs:
                obs.append((n-1,i))
        return obs


    def random_generate(self):
        nb = (self.mapsize[0]*self.mapsize[1]) // self.blocksize
        cnt = 0
        while cnt < nb:
            x = randint(1, self.mapsize[0]-2)
            y = randint(1, self.mapsize[1]-2)
            if (x, y) not in self.obs and (x,y) != (1,1) and (x,y) != (self.mapsize[0]-2, self.mapsize[1]-2):
                self.obs.append((x,y))
            cnt += 1

    def add_obs(self, p):
        if p in self.obs or p == self.s or p == self.g:
            print(p+"已是障碍物")
            return 0
        else:
            self.obs.append(p)
            return 1


if __name__ == "__main__":
    m = Map((10,10))
    print(m.obs)