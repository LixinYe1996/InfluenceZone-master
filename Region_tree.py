import math
import sys


# B = 4
class Rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def perimeter(self):
        return 2 * (abs(self.x2 - self.x1) + abs(self.y2 - self.y1))

    def is_overlap(self, rect):
        if self.y1 > rect.y2 or self.y2 < rect.y1 or self.x1 > rect.x2 or self.x2 < rect.x1:
            return False
        return True

    def contain_rect(self, rect):
        return self.x1 < rect.x1 and self.y1 < rect.y1 and self.x2 > rect.x2 and self.y2 > rect.y2

    def has_point(self, point):
        return self.x1 <= point.x <= self.x2 and self.y1 <= point.y <= self.y2

    def __str__(self):
        return "Rect: ({}, {}), ({}, {})".format(self.x1, self.y1, self.x2, self.y2)


class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "Point #{}: ({}, {})".format(self.id, self.x, self.y)


class Segment:
    def __init__(self, spoint, epoint):
        self.spoint = spoint
        self.epoint = epoint

    def __str__(self):
        return "Segment #({}, {})".format(self.spoint, self.epoint)


class Line:
    def __int__(self, m, c):
        self.m = m
        self.c = c

    def __str__(self):
        return "Line #({}, {})".format(self.m, self.c)


def sequential_query(points, query):
    result = 0
    for point in points:
        if query.x1 <= point.x <= query.x2 and query.y1 <= point.y <= query.y2:
            result = result + 1
    return result


class Node(object):
    def __init__(self, B):
        self.B = B
        self.id = 0
        # 非叶子节点
        self.child_nodes = []
        # 叶子节点
        self.data_points = []
        self.parent_node = None
        # 最小边界矩形
        self.MBR = Rect(-1, -1, -1, -1)

    def add_point(self, point):
        # 添加点 保持点在正确的位置
        # update in the right position to keep the list ordered
        self.add_points([point])
        pass

    def add_points(self, points):
        self.data_points += points
        # 更新最小边界矩形
        # update MBR
        self.update_MBR()
        pass

    def perimeter_increase_with_point(self, point):
        # 周长改变 随着加入的点
        x1 = point.x if point.x < self.MBR.x1 else self.MBR.x1
        y1 = point.y if point.y < self.MBR.y1 else self.MBR.y1
        x2 = point.x if point.x > self.MBR.x2 else self.MBR.x2
        y2 = point.y if point.y > self.MBR.y2 else self.MBR.y2
        return Rect(x1, y1, x2, y2).perimeter() - self.perimeter()

    def perimeter(self):
        # 返回周长的一半
        # only calculate the half perimeter here
        return self.MBR.perimeter()

    def is_underflow(self):
        # 是否
        return (self.is_leaf() and len(self.data_points) < math.ceil(self.B / 2)) or \
               (not self.is_leaf() and len(self.child_nodes) < math.ceil(self.B / 2))

    def is_overflow(self):
        # 节点是否溢出
        return (self.is_leaf() and len(self.data_points) > self.B) or \
               (not self.is_leaf() and len(self.child_nodes) > self.B)

    def is_root(self):
        # 是否根节点
        return self.parent_node is None

    def is_intermediate(self):
        if len(self.child_nodes) != 0 and len(self.data_points) == 0:
            return True
        else:
            return False

    def is_leaf(self):
        # 是否叶子节点
        return len(self.child_nodes) == 0

    def add_child_node(self, node):
        # 添加孩子节点
        self.add_child_nodes([node])
        pass

    def add_child_nodes(self, nodes):
        for node in nodes:
            node.parent_node = self
            self.child_nodes.append(node)
        # 更新最小边界矩形
        self.update_MBR()
        pass

    def update_MBR(self):
        # 更新最小边界矩形
        if self.is_leaf():
            # 是叶子节点 找数据节点中的所有节点的最小边界矩形
            self.MBR.x1 = min([point.x for point in self.data_points])
            self.MBR.x2 = max([point.x for point in self.data_points])
            self.MBR.y1 = min([point.y for point in self.data_points])
            self.MBR.y2 = max([point.y for point in self.data_points])
        else:
            # 非叶子节点 找孩子节点中所有孩子节点的最小边界矩形
            self.MBR.x1 = min([child.MBR.x1 for child in self.child_nodes])
            self.MBR.x2 = max([child.MBR.x2 for child in self.child_nodes])
            self.MBR.y1 = min([child.MBR.y1 for child in self.child_nodes])
            self.MBR.y2 = max([child.MBR.y2 for child in self.child_nodes])
        if self.parent_node and not self.parent_node.MBR.contain_rect(self.MBR):
            # 若父节点非空 且父节点不包含自己的最小边界矩形 则进行更新（递归）
            self.parent_node.update_MBR()
        pass

    # Get perimeter of an MBR formed by a list of data points
    @staticmethod
    def get_points_MBR_perimeter(points):
        # 获得point列表的最小边界矩形
        x1 = min([point.x for point in points])
        x2 = max([point.x for point in points])
        y1 = min([point.y for point in points])
        y2 = max([point.y for point in points])
        return Rect(x1, y1, x2, y2).perimeter()

    @staticmethod
    def get_nodes_MBR_perimeter(nodes):
        # 获得node列表的最小边界矩形
        x1 = min([node.MBR.x1 for node in nodes])
        x2 = max([node.MBR.x2 for node in nodes])
        y1 = min([node.MBR.y1 for node in nodes])
        y2 = max([node.MBR.y2 for node in nodes])
        return Rect(x1, y1, x2, y2).perimeter()


class RegionTree:
    def __init__(self, B=4):
        self.B = B
        self.root = Node(self.B)

    def insert_point(self, point, cur_node=None):
        # init U as node
        # print("{} is leaf: {}".format(self.root, self.root.is_leaf()))

        if cur_node is None:
            # 设置为根节点
            cur_node = self.root
            # print("{} is leaf: {}".format(cur_node, cur_node.is_leaf()))
        # Insertion logic start
        if cur_node.is_leaf():
            # 若为叶子节点 将点加入该节点
            cur_node.add_point(point)
            # handle overflow  溢出检查
            if cur_node.is_overflow():
                # 调用溢出处理 splitnode算法 将该节点分裂两个节点
                self.handle_overflow(cur_node)
        else:
            # 若非叶子节点 调用chooseleaf 选择最佳插入节点
            chosen_child = self.choose_best_child(cur_node, point)
            self.insert_point(point, cur_node=chosen_child)

    # Find a suitable one to expand:
    @staticmethod
    def choose_best_child(node, point):
        best_child = None
        best_perimeter = 0
        # Scan the child nodes 查找子节点 找到当插入需要插入的记录后面积过大最小的那个节点
        for item in node.child_nodes:

            if node.child_nodes.index(item) == 0 or best_perimeter > item.perimeter_increase_with_point(point):
                # print("choose_best_child")
                # print(node.child_nodes.index(item))

                best_child = item
                best_perimeter = item.perimeter_increase_with_point(point)
        return best_child

    # WIP
    def handle_overflow(self, node):
        # 处理溢出 若为叶子节点 调用split_leaf_node 若非叶子节点 调用split_internal_node 分裂出L和LL
        node, new_node = self.split_leaf_node(node) if node.is_leaf() else self.split_internal_node(node)

        # 若其中一个节点为根节点 则将创建一个新的根节点 并将L和LL加入该节点
        if self.root is node:
            self.root = Node(self.B)
            self.root.add_child_nodes([node, new_node])
        else:
            # 若非根节点 将新增节点 插入父节点 并递归进行溢出检查
            node.parent_node.add_child_node(new_node)
            if node.parent_node.is_overflow():
                self.handle_overflow(node.parent_node)

    # WIP  叶子节点分裂算法 将M+1条记录 分裂成两组 M设为4 线性分裂和平方分裂 分裂后的两个节点的最小边界矩形 应尽可能的小
    # 尝试但不确保 没有穷举
    def split_leaf_node(self, node):
        m = len(node.data_points)
        best_perimeter = -1
        best_set_1 = []
        best_set_2 = []
        # Run x axis 按x排序 找最高最低边
        # find extreme rectangle along all dimensions .All each dimension ,find the entry whose
        # rectangle has highest low side  ,and the one with lowset high side  Record the separation.
        # adjust for shape of the rectangle cluster .normalize the separations by dividing by the width of the
        # entire set along the corresponding dimension
        # select the most extreme pair  .choose the pair with the greatest normalized separation with
        # any dimension
        # 在所有尺寸上找到最小边界矩形。在所有尺寸上，找到矩形的最低边最高，而高边最低的条目。记录间隔。
        # 调整矩形簇的形状。除以沿相应尺寸的整个集合的宽度，将间隔归一化。
        # 选择最极端的对。选择任何尺寸的归一化间隔最大的对。
        all_point_sorted_by_x = sorted(node.data_points, key=lambda point: point.x)

        for i in range(int(0.4 * m), int(m * 0.6) + 1):
            list_point_1 = all_point_sorted_by_x[:i]
            list_point_2 = all_point_sorted_by_x[i:]
            temp_sum_perimeter = Node.get_points_MBR_perimeter(list_point_1) \
                                 + Node.get_points_MBR_perimeter(list_point_2)
            if best_perimeter == -1 or best_perimeter > temp_sum_perimeter:
                best_perimeter = temp_sum_perimeter
                best_set_1 = list_point_1
                best_set_2 = list_point_2
        # Run y axis
        all_point_sorted_by_y = sorted(node.data_points, key=lambda point: point.y)
        for i in range(int(0.4 * m), int(m * 0.6) + 1):
            list_point_1 = all_point_sorted_by_y[:i]
            list_point_2 = all_point_sorted_by_y[i:]
            temp_sum_perimeter = Node.get_points_MBR_perimeter(list_point_1) \
                                 + Node.get_points_MBR_perimeter(list_point_2)
            if best_perimeter == -1 or best_perimeter > temp_sum_perimeter:
                best_perimeter = temp_sum_perimeter
                best_set_1 = list_point_1
                best_set_2 = list_point_2
        node.data_points = best_set_1
        node.update_MBR()
        new_node = Node(self.B)
        new_node.add_points(best_set_2)
        return node, new_node

    # WIP
    def split_internal_node(self, node):
        m = len(node.child_nodes)
        best_perimeter = -1
        best_set_1 = []
        best_set_2 = []
        # Run x axis
        all_node_sorted_by_x = sorted(node.child_nodes, key=lambda child: child.MBR.x1)
        for i in range(int(0.4 * m), int(m * 0.6) + 1):
            list_node_1 = all_node_sorted_by_x[:i]
            list_node_2 = all_node_sorted_by_x[i:]
            temp_sum_perimeter = Node.get_nodes_MBR_perimeter(list_node_1) \
                                 + Node.get_nodes_MBR_perimeter(list_node_2)
            if best_perimeter == -1 or best_perimeter > temp_sum_perimeter:
                best_perimeter = temp_sum_perimeter
                best_set_1 = list_node_1
                best_set_2 = list_node_2
                # Run y axis
        all_node_sorted_by_y = sorted(node.child_nodes, key=lambda child: child.MBR.y1)
        for i in range(int(0.4 * m), int(m * 0.6) + 1):
            list_node_1 = all_node_sorted_by_y[:i]
            list_node_2 = all_node_sorted_by_y[i:]
            temp_sum_perimeter = Node.get_nodes_MBR_perimeter(list_node_1) \
                                 + Node.get_nodes_MBR_perimeter(list_node_2)
            if best_perimeter == -1 or best_perimeter > temp_sum_perimeter:
                best_perimeter = temp_sum_perimeter
                best_set_1 = list_node_1
                best_set_2 = list_node_2
        node.child_nodes = best_set_1
        node.update_MBR()
        new_node = Node(self.B)
        new_node.add_child_nodes(best_set_2)
        return node, new_node

    # Take in a Rect and return number of data point that is covered by the R tree.
    def region_query(self, rect, node=None):
        # initiate with root
        if node is None:
            node = self.root

        if node.is_leaf():
            # print("get here")
            count = 0
            for point in node.data_points:
                if rect.has_point(point):
                    count += 1
            return count
        else:
            # print([child.MBR for child in node.child_nodes])
            total = 0
            for child in node.child_nodes:
                # print("{} and {} is overlapped {}".format(rect, child.MBR, rect.is_overlap(child.MBR)))
                if rect.is_overlap(child.MBR):
                    total += self.region_query(rect, child)
            return total

    def print_tree(self, cur_node=None):
        if cur_node is None:
            cur_node = self.root
        if cur_node.is_leaf():
            print("叶子节点 ")
            for i in range(len(cur_node.data_points)):
                print(cur_node.data_points[i])
            return
        else:
            print("中间节点")
            print("最小边界矩形", cur_node.MBR.x1, cur_node.MBR.x2, cur_node.MBR.y1, cur_node.MBR.y2)
            for i in range(len(cur_node.child_nodes)):
                self.print_tree(cur_node.child_nodes[i])

    def delete_point(self, point, cur_node=None):
        self.findleaf(point, cur_node)
        pass


def test_the_shit():
    tree = RegionTree(2)
    import random
    for i in range(15):
        tree.insert_point(Point(random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)))
    Rect(57144, 24954, 58144, 25954).is_overlap(Rect(1, 52163, 100000, 100000))
    pass
