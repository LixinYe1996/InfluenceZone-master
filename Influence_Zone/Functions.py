import Region_tree


def dist(p, q):
    """
    根据p的类型返回p,q的距离 若为point 若为最小边界矩形
    :param p:
    :param q:
    :return: dist(p,q)
    """
    # print("p的类型",type(p))
    if type(p) == Region_tree.Node:
        if q.x <= p.MBR.x2 and q.x >= p.MBR.x1 and q.y <= p.MBR.y2 and q.y >= p.MBR.y1:
            return 0
        else:
            return (min((p.MBR.x1 - q.x) ** 2, (p.MBR.x2 - q.x) ** 2) + min((p.MBR.y1 - q.y) ** 2, (
                    p.MBR.y2 - q.y) ** 2)) ** 0.5
    else:
        return ((p.x - q.x) ** 2 + (p.y - q.y) ** 2) ** 0.5
