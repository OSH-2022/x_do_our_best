import itertools
import ray
import timeit

ray.init()

@ray.remote
def distance(x1, y1, x2, y2):
    ans = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    return ans


@ray.remote
def shortest_way(Location, n):
    dis = [[0.0] * 1005] * 1005
    #找到所给坐标点的最短访问序列，并返回调整过的坐标序列
    min_dis = 10000000000000
    for i in range(0, n):
        for j in range(0, n):
            dis[i][j] = (Location[2 * i] - Location[2 * j]) * (Location[2 * i] - Location[2 * j]) + (Location[2 * i + 1] - Location[2 * j + 1]) * (Location[2 * i + 1] - Location[2 * j + 1])
    nums = []
    for i in range(0, n):
        nums.append(i)
    print(nums)
    for num in itertools.permutations(nums, n): #逐个生成各个点序号的全排列
        print(num)
        route_dis = 0.0
        for j in range(0, n - 1):
            route_dis = route_dis + (Location[2 * num[j]] - Location[2 * num[j + 1]]) * (Location[2 * num[j]] - Location[2 * num[j + 1]]) + (Location[2 * num[j] + 1] - Location[2 * num[j + 1] + 1]) * (Location[2 * num[j] + 1] - Location[2 * num[j + 1] + 1])
        print(route_dis)
        if route_dis < min_dis:
            min_dis = route_dis
            route = num

    return route


Location = [[1.5, 2.4, 3.2, 1.5, 2.8, 4.5, 8.3, 3.6, 4.8, 5.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [3.5, 1.4, 6.2, 9.5, 1.8, 3.5, 6.3, 2.6, 7.8, 2.0]
, [6.5, 5.4, 5.2, 5.5, 4.8, 6.5, 1.3, 1.6, 3.8, 2.0]
, [2.5, 1.4, 3.2, 3.5, 7.8, 4.5, 7.3, 6.6, 6.8, 5.0]
, [7.5, 7.4, 5.2, 4.5, 3.8, 2.5, 4.3, 3.6, 2.8, 2.0]
, [1.5, 3.4, 8.2, 2.5, 6.8, 7.5, 8.3, 9.6, 8.8, 6.0]
, [8.5, 8.4, 4.2, 6.5, 3.8, 4.5, 4.3, 3.6, 3.8, 2.0]
, [3.5, 3.4, 5.2, 4.5, 8.8, 7.5, 8.3, 5.6, 5.8, 7.0]
, [5.5, 5.4, 7.2, 3.5, 2.8, 4.5, 2.3, 8.6, 3.8, 3.0]
, [3.5, 3.4, 6.2, 7.5, 8.8, 8.5, 4.3, 5.6, 8.8, 5.0]
, [2.5, 8.4, 3.2, 5.5, 4.8, 3.5, 3.3, 4.6, 4.8, 3.0]
, [7.5, 2.4, 8.2, 4.5, 6.8, 5.5, 7.3, 8.6, 2.8, 2.0]
, [6.5, 9.4, 4.2, 8.5, 2.8, 2.5, 5.3, 3.6, 8.8, 7.0]
, [3.5, 4.4, 5.2, 9.5, 8.8, 8.5, 9.3, 6.6, 4.8, 3.0]
, [9.5, 9.4, 2.2, 3.5, 5.8, 4.5, 6.3, 5.6, 6.8, 7.0]
, [0.5, 4.4, 8.2, 4.5, 4.8, 8.5, 4.3, 3.6, 7.8, 5.0]
, [3.5, 6.4, 5.2, 5.5, 8.8, 5.5, 6.3, 8.6, 4.8, 4.0]
, [5.5, 3.4, 4.2, 7.5, 5.8, 4.5, 3.3, 5.6, 2.8, 3.0]
, [4.5, 8.4, 7.2, 2.5, 4.8, 8.5, 6.3, 2.6, 1.8, 6.0]
, [1.5, 2.4, 5.2, 9.5, 7.8, 2.5, 4.3, 9.6, 9.8, 2.0]]

def fun():
    id0 = shortest_way.remote(Location[0], 5)
    id1 = shortest_way.remote(Location[1], 5)
    id2 = shortest_way.remote(Location[2], 5)
    id3 = shortest_way.remote(Location[3], 5)
    id4 = shortest_way.remote(Location[4], 5)

    re0 = ray.get(id0)
    re1 = ray.get(id1)
    re2 = ray.get(id2)
    re3 = ray.get(id3)
    re4 = ray.get(id4)


    print(re0, re1, re2, re3, re4)

time = timeit.timeit('fun()', 'from __main__ import fun', number=1)
print("time =", time)