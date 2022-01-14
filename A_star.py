import sys
import math
from point import Point
from map import Map
import pygame
from color import *

CELL_WIDTH = 16 #单元格宽度
CELL_HEIGHT = 16 #单元格长度
BORDER_WIDTH = 1 #边框宽度
mapsize = [20, 20]

class AStar:
    def __init__(self, start, goal, map):
        self.s = start
        self.g = goal
        self.s.G = 0
        self.s.H = self.H(start)
        self.s.F = self.s.H

        self.map = map
        self.open = []
        self.close = []
        self.directions = [(i,j) for i in [0,-1,1] for j in [0,-1,1] if i*j == 0]
        self.directions.remove((0,0))
        self.open.append(self.s)

    def H(self, p):
        '''
        启发函数，计算p到goal的预计距离，使用曼哈顿距离
        :param p: 当前位置
        :return: 预计距离
        '''
        dx = abs(self.g.x-p.x)
        dy = abs(self.g.y-p.y)
        return min(dx, dy) * 2 + abs(dx-dy)

    def get_neighbors(self, p):
        return [p.move(d) for d in self.directions if p.move(d) not in self.map.obs]

    def get_minF(self):
        self.open.sort(key=lambda x: x.F)
        return self.open.pop(0)

    def find(self, p):
        for i, n in enumerate(self.open):
            if n == p:
                return i, n

    def update(self, p):
        p.G = p.father.G + 1
        p.H = self.H(p)
        p.F = p.G + p.H

    def run(self):
        flag = 0
        self.route = []
        while len(self.open) > 0:
            frontier = self.get_minF()
            # print(frontier)

            for c in self.get_neighbors(frontier):
                p = Point(c[0],c[1])
                p.father = frontier
                p.G = frontier.G + 1
                p.F = p.G + self.H(p)
                # 当前节点为终点
                if p == self.g:
                    while p.father != self.s:
                        print(p.father)
                        self.route.append((p.father.x, p.father.y))
                        p = p.father

                    flag = 1
                    break
                # 当前节点已遍历过
                elif p in self.close:
                    continue
                # 当前节点待遍历
                elif p in self.open:
                    i, n = self.find(p)
                    if p.G < n.G:
                        n.father = frontier
                        self.update(n)

                else:
                    self.open.append(p)
            self.close.append(frontier)
            if flag == 1:
                break



    def plot(self):
        pygame.init()
        # 此处要将地图投影大小转换为像素大小，此处设地图中每个单元格的大小为CELL_WIDTH*CELL_HEIGHT像素
        # mymap = Map((mapsize[0] * CELL_WIDTH, mapsize[1] * CELL_HEIGHT))
        pix_sn = (self.s.x * CELL_WIDTH, self.s.y * CELL_HEIGHT)
        pix_en = (self.g.x * CELL_WIDTH, self.g.y * CELL_HEIGHT)
        # 对blocklist和routelist中的坐标同样要转换为像素值

        def transform(x):
            return (x[0] * CELL_WIDTH, x[1] * CELL_HEIGHT)

        bl_pix = [transform(x) for x in self.map.obs]
        rl_pix = [((x[0]+0.5) * CELL_WIDTH, (x[1]+0.5) * CELL_HEIGHT) for x in self.route]
        # 初始化显示的窗口并设置尺寸
        screen = pygame.display.set_mode(transform(mapsize))
        # 设置窗口标题
        pygame.display.set_caption('A*算法路径搜索演示：')
        # 用白色填充屏幕
        screen.fill(Color.WHITE.value)  # 为什么用参数Color.WHITE不行？

        # 绘制屏幕中的所有单元格
        for (x, y) in [(i*CELL_WIDTH, j*CELL_HEIGHT) for i in range(mapsize[0]) for j in range(mapsize[1])]:
            if (x, y) in bl_pix:
                # 绘制黑色的障碍物单元格，并留出2个像素的边框
                pygame.draw.rect(screen, Color.BLACK.value, (
                (x + BORDER_WIDTH, y + BORDER_WIDTH), (CELL_WIDTH - 2 * BORDER_WIDTH, CELL_HEIGHT - 2 * BORDER_WIDTH)))
            else:
                # 绘制绿色的可通行单元格，并留出2个像素的边框
                pygame.draw.rect(screen, Color.GREEN.value, (
                (x + BORDER_WIDTH, y + BORDER_WIDTH), (CELL_WIDTH - 2 * BORDER_WIDTH, CELL_HEIGHT - 2 * BORDER_WIDTH)))
        # 绘制起点和终点
        pygame.draw.circle(screen, Color.BLUE.value, (pix_sn[0] + CELL_WIDTH // 2, pix_sn[1] + CELL_HEIGHT // 2),
                           CELL_WIDTH // 2 - 1)
        pygame.draw.circle(screen, Color.RED.value, (pix_en[0] + CELL_WIDTH // 2, pix_en[1] + CELL_HEIGHT // 2),
                           CELL_WIDTH // 2 - 1)

        # 绘制搜索得到的最优路径
        if self.route:
            pygame.draw.aalines(screen, Color.RED.value, False, rl_pix)
        else:
            print("未找到可行解")
        keepGoing = True
        while keepGoing:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
            pygame.display.flip()


if __name__ == "__main__":
    s = Point(1,1)
    g = Point(mapsize[0]-2,mapsize[1]-2)
    map = Map(mapsize, blocksize=4)
    a = AStar(s, g, map)
    a.run()

    a.plot()
    while True:
        if not a.route:
            break
        i = input("请输入障碍点坐标,格式如'2,3',不需要引号, 输入q退出\n")
        if i == 'q':
            break
        x, y = [int(s) for s in i.split(',')]
        f = map.add_obs((x,y))
        if not f:
            continue
        else:
            a = AStar(s, g, map)
            a.run()
            a.plot()



