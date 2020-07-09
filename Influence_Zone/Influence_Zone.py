from Influence_Zone.Heap import HeapPriorityQueue
from Influence_Zone.Intersection import intersection
from Influence_Zone.Perendicular_bisector import perendicular_bisector
from Influence_Zone.Functions import dist
from Region_tree import Point
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull


class Influence_zone:
    def __init__(self):
        self.rmin = float("inf")
        self.rmax = 0
        self.zone = []
        # 影响区凸多边形 为Point序列
        self.bisector = []
        # 用于修剪空间的垂直平分线 为Line序列（m,c）y=mx+c
        self.intersect = []
        # 交点集合 由垂直平分线和 边界的交点组成 同时还包含每个交点的计数器（Point,count）
        self.eindex = []
        self.query_point = None
        self.k = None
        # 用于修剪空间的对象e的序列 由point组成

    def compute(self, query_point, root, k, bound, Obeject_set):
        # 将R-tree的root加入min-heap中
        self.query_point = query_point
        self.k = k
        k = k + 1
        # 计算rknn时需计算Zk+1影响区
        minheap = HeapPriorityQueue()
        minheap.add(-1, root)
        self.zone = [Point(-1, 0, 0), Point(-1, 0, bound), Point(-1, bound, 0), Point(-1, bound, bound)]
        self.intersect = [[Point(-1, 0, 0), 0], [Point(-1, bound, 0), 0], [Point(-1, 0, bound), 0],
                          [Point(-1, bound, bound), 0]]
        prun_time = 1
        node_num = 1
        while minheap:
            # 取堆顶元素
            key, e = minheap.min()
            # for item in minheap._data:
            #     print(item)
            # 将堆顶元素去堆
            minheap.remove_min()
            valid = None
            # 判断节点有效性
            if dist(e, query_point) < 2 * self.rmin:
                valid = True
            elif dist(e, query_point) > 2 * self.rmax:
                valid = False
            # 对于zone中的每个凸顶点
            if valid == None:
                for v in self.zone:
                    if dist(e, v) < dist(query_point, v):
                        valid = True
                        break
            if valid == True:
                if type(e) == type(query_point):

                    prun_time = prun_time + 1
                    # 改为增量更新
                    self.eindex.append(e)
                    # 计算垂直平分线
                    tbisector = perendicular_bisector().generate(query_point, [e])
                    # bisector = perendicular_bisector().generate(query_point, self.eindex)
                    # 计算交点
                    self.intersect = intersection().generate(self.bisector, tbisector, bound, query_point, self.eindex,
                                                             self.intersect)
                    self.bisector.extend(tbisector)
                    # 计算凸包1
                    # points=[]
                    # for i in range(len(intersect)):
                    #     if intersect[i][1]<k:
                    #         #若计数器小于k 未修剪区域由计数器小于k的点组成
                    #         points.append([intersect[i][0].x,intersect[i][0].y])
                    # points=np.array(points)
                    # 计算凸包2
                    # 在不在数据空间边界的交点中，只有计数器等于k-1的交点可以是凸顶点

                    # 只有每条边界线的两个极值点可以是凸点
                    # 上下左右边界上凸顶点
                    points = []
                    for i in range(len(self.intersect)):
                        if self.intersect[i][1] < k:
                            if self.intersect[i][1] == k - 1:
                                # 若计数器小于k 未修剪区域由计数器小于k的点组成
                                # print(intersect[i][0])
                                points.append([self.intersect[i][0].x, self.intersect[i][0].y])
                                continue
                            if abs(self.intersect[i][0].x - bound) < 0.01 or abs(
                                    self.intersect[i][0].y - bound) < 0.01 or abs(
                                    self.intersect[i][0].x - 0) < 0.01 or abs(self.intersect[i][0].y - 0) < 0.01:
                                # 若计数器小于k 未修剪区域由计数器小于k的点组成
                                # print(intersect[i][0])
                                points.append([self.intersect[i][0].x, self.intersect[i][0].y])
                                continue

                    #######################
                    points = np.array(points)
                    hull = ConvexHull(points)
                    Obeject_set.append(query_point)
                    # draw_scatter(Obeject_set, self.bisector, bound, self.intersect, hull, points)
                    zone = []
                    hull1 = hull.vertices.tolist()
                    z = 0
                    for i in hull1:
                        z = z + 1
                        zone.append(Point(-1, points[i][0], points[i][1]))
                    # print(e, "数据节点修剪空间", prun_time)
                    # print(len(self.intersect), len(points), z)
                    # print(self.rmax, self.rmin)
                    self.zone = zone
                    self.rmin = get_rmin(query_point, self.zone)
                    self.rmax = get_rmax(query_point, self.zone)

                    continue
                if e.is_leaf():
                    node_num = node_num + 1
                    # print("Nodes accesses=",node_num)
                    for i in range(len(e.data_points)):
                        r = dist(e.data_points[i], query_point)
                        minheap.add(r, e.data_points[i])
                if e.is_intermediate():
                    node_num = node_num + 1
                    # print("Nodes accesses",node_num)
                    for i in range(len(e.child_nodes)):
                        r = dist(e.child_nodes[i], query_point)
                        minheap.add(r, e.child_nodes[i])

    def rknn(self):
        rknnpoints = []
        # rknn候选集
        for e in self.eindex:
            count = 0
            for p in self.eindex:
                if e == p:
                    continue
                if dist(e, p) < dist(e, self.query_point):
                    count = count + 1
            if count < self.k:
                rknnpoints.append(e)
        return rknnpoints


def get_rmin(q, zone):
    rmin = float("inf")
    for i in range(len(zone) - 1):
        midpoint = Point(-1, (zone[i].x + zone[i + 1].x) / 2, (zone[i].y + zone[i + 1].y) / 2)
        r = dist(midpoint, q)
        if r < rmin:
            rmin = r
    return rmin


def get_rmax(q, zone):
    rmax = 0
    for e in zone:
        r = dist(e, q)
        if r > rmax:
            rmax = r
    return rmax


def draw_scatter(Obeject_set, bisector, bound, intersect, hull, points):
    """
    绘制点和垂直平分线
    :param Obeject_set: 点集
    :param bisector: 垂直平分线集
    :param bound: 边界
    :return:
    """
    hull1 = hull.vertices.tolist()  # 要闭合必须再回到起点[0]
    hull1.append(hull1[0])

    x1 = []
    y1 = []
    id = []
    for i in range(len(Obeject_set)):
        x1.append(Obeject_set[i].x)
        y1.append(Obeject_set[i].y)
        id.append(Obeject_set[i].id)
    #
    x2 = []
    y2 = []
    count = []
    for i in range(len(intersect)):
        x2.append(intersect[i][0].x)
        y2.append(intersect[i][0].y)
        count.append(intersect[i][1])
    fig = plt.figure(figsize=(6, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.scatter(x1, y1, c='k', marker='.')
    plt.xlim(0 - 0.1, bound + 0.1)
    plt.ylim(0 - 0.1, bound + 0.1)

    ax1.scatter(x2, y2, c='b', marker='.')

    for i in range(len(bisector)):
        # print(bisector[i].m,bisector[i].c)
        if bisector[i].m == float('inf'):
            ax1.axvline(x=bisector[i].c, ls="-")  # 垂直直线
        else:
            x = np.linspace(0, bound, 100)
            y = bisector[i].m * x + bisector[i].c
            ax1.plot(x, y)
    ax1.plot(points[hull1, 0], points[hull1, 1], 'r--^', lw=2)
    for i in range(len(id)):
        ax1.text(x1[i], y1[i], id[i], color="k")
    for i in range(len(count)):
        ax1.text(x2[i], y2[i], count[i], color="b")
    plt.show()
