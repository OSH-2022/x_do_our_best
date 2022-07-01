import itertools
import ray
import cProfile
import timeit
import tracemalloc


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
    #print(nums)
    for num in itertools.permutations(nums, n): #逐个生成各个点序号的全排列
        #print(num)
        route_dis = 0.0
        for j in range(0, n - 1):
            route_dis = route_dis + (Location[2 * num[j]] - Location[2 * num[j + 1]]) * (Location[2 * num[j]] - Location[2 * num[j + 1]]) + (Location[2 * num[j] + 1] - Location[2 * num[j + 1] + 1]) * (Location[2 * num[j] + 1] - Location[2 * num[j + 1] + 1])
        #print(route_dis)
        if route_dis < min_dis:
            min_dis = route_dis
            route = num

    return route

@ray.remote
def merge_route(route1, route2):
    length1 = len(route1)
    length2 = len(route2)
    i = 0
    j = 0
    new_route = []
    while i < length1 and j < length2:

        new_route.append(route1[i])
        new_route.append(route2[j])
        i = i + 1
        j = j + 1

    while i < length1:

        new_route.append(route1[i])
        i = i + 1

    while j < length2:

        new_route.append(route2[i])
        j = j + 1


    return new_route


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
    route0 = shortest_way.remote(Location[0], 5)
    route1 = shortest_way.remote(Location[1], 5)
    new_route1 = merge_route.remote(route0, route1)
    route2 = shortest_way.remote(Location[2], 5)
    new_route2 = merge_route.remote(new_route1, route2)
    route3 = shortest_way.remote(Location[3], 5)
    new_route3 = merge_route.remote(new_route2, route3)
    route4 = shortest_way.remote(Location[4], 5)
    new_route4 = merge_route.remote(new_route3, route4)
    route5 = shortest_way.remote(Location[4], 5)
    new_route5 = merge_route.remote(new_route4, route5)

    aroute0 = shortest_way.remote(Location[0], 5)
    aroute1 = shortest_way.remote(Location[1], 5)
    anew_route1 = merge_route.remote(aroute0, aroute1)
    aroute2 = shortest_way.remote(Location[2], 5)
    anew_route2 = merge_route.remote(anew_route1, aroute2)
    aroute3 = shortest_way.remote(Location[3], 5)
    anew_route3 = merge_route.remote(anew_route2, aroute3)
    aroute4 = shortest_way.remote(Location[4], 5)
    anew_route4 = merge_route.remote(anew_route3, aroute4)
    aroute5 = shortest_way.remote(Location[4], 5)
    anew_route5 = merge_route.remote(anew_route4, aroute5)

    broute0 = shortest_way.remote(Location[0], 5)
    broute1 = shortest_way.remote(Location[1], 5)
    bnew_route1 = merge_route.remote(broute0, broute1)
    broute2 = shortest_way.remote(Location[2], 5)
    bnew_route2 = merge_route.remote(bnew_route1, broute2)
    broute3 = shortest_way.remote(Location[3], 5)
    bnew_route3 = merge_route.remote(bnew_route2, broute3)
    broute4 = shortest_way.remote(Location[4], 5)
    bnew_route4 = merge_route.remote(bnew_route3, broute4)
    broute5 = shortest_way.remote(Location[4], 5)
    bnew_route5 = merge_route.remote(bnew_route4, broute5)

    croute0 = shortest_way.remote(Location[0], 5)
    croute1 = shortest_way.remote(Location[1], 5)
    cnew_route1 = merge_route.remote(croute0, croute1)
    croute2 = shortest_way.remote(Location[2], 5)
    cnew_route2 = merge_route.remote(cnew_route1, croute2)
    croute3 = shortest_way.remote(Location[3], 5)
    cnew_route3 = merge_route.remote(cnew_route2, croute3)
    croute4 = shortest_way.remote(Location[4], 5)
    cnew_route4 = merge_route.remote(cnew_route3, croute4)
    croute5 = shortest_way.remote(Location[4], 5)
    cnew_route5 = merge_route.remote(cnew_route4, croute5)

    droute0 = shortest_way.remote(Location[0], 5)
    droute1 = shortest_way.remote(Location[1], 5)
    dnew_route1 = merge_route.remote(droute0, droute1)
    droute2 = shortest_way.remote(Location[2], 5)
    dnew_route2 = merge_route.remote(dnew_route1, droute2)
    droute3 = shortest_way.remote(Location[3], 5)
    dnew_route3 = merge_route.remote(dnew_route2, droute3)
    droute4 = shortest_way.remote(Location[4], 5)
    dnew_route4 = merge_route.remote(dnew_route3, droute4)
    droute5 = shortest_way.remote(Location[4], 5)
    dnew_route5 = merge_route.remote(dnew_route4, droute5)

    eroute0 = shortest_way.remote(Location[0], 5)
    eroute1 = shortest_way.remote(Location[1], 5)
    enew_route1 = merge_route.remote(eroute0, eroute1)
    eroute2 = shortest_way.remote(Location[2], 5)
    enew_route2 = merge_route.remote(enew_route1, eroute2)
    eroute3 = shortest_way.remote(Location[3], 5)
    enew_route3 = merge_route.remote(enew_route2, eroute3)
    eroute4 = shortest_way.remote(Location[4], 5)
    enew_route4 = merge_route.remote(enew_route3, eroute4)
    eroute5 = shortest_way.remote(Location[4], 5)
    enew_route5 = merge_route.remote(enew_route4, eroute5)

    froute0 = shortest_way.remote(Location[0], 5)
    froute1 = shortest_way.remote(Location[1], 5)
    fnew_route1 = merge_route.remote(froute0, froute1)
    froute2 = shortest_way.remote(Location[2], 5)
    fnew_route2 = merge_route.remote(fnew_route1, froute2)
    froute3 = shortest_way.remote(Location[3], 5)
    fnew_route3 = merge_route.remote(fnew_route2, froute3)
    froute4 = shortest_way.remote(Location[4], 5)
    fnew_route4 = merge_route.remote(fnew_route3, froute4)
    froute5 = shortest_way.remote(Location[4], 5)
    fnew_route5 = merge_route.remote(fnew_route4, froute5)

    groute0 = shortest_way.remote(Location[0], 5)
    groute1 = shortest_way.remote(Location[1], 5)
    gnew_route1 = merge_route.remote(groute0, groute1)
    groute2 = shortest_way.remote(Location[2], 5)
    gnew_route2 = merge_route.remote(gnew_route1, groute2)
    groute3 = shortest_way.remote(Location[3], 5)
    gnew_route3 = merge_route.remote(gnew_route2, groute3)
    groute4 = shortest_way.remote(Location[4], 5)
    gnew_route4 = merge_route.remote(gnew_route3, groute4)
    groute5 = shortest_way.remote(Location[4], 5)
    gnew_route5 = merge_route.remote(gnew_route4, groute5)

    hroute0 = shortest_way.remote(Location[0], 5)
    hroute1 = shortest_way.remote(Location[1], 5)
    hnew_route1 = merge_route.remote(hroute0, hroute1)
    hroute2 = shortest_way.remote(Location[2], 5)
    hnew_route2 = merge_route.remote(hnew_route1, hroute2)
    hroute3 = shortest_way.remote(Location[3], 5)
    hnew_route3 = merge_route.remote(hnew_route2, hroute3)
    hroute4 = shortest_way.remote(Location[4], 5)
    hnew_route4 = merge_route.remote(hnew_route3, hroute4)
    hroute5 = shortest_way.remote(Location[4], 5)
    hnew_route5 = merge_route.remote(hnew_route4, hroute5)

    iroute0 = shortest_way.remote(Location[0], 5)
    iroute1 = shortest_way.remote(Location[1], 5)
    inew_route1 = merge_route.remote(iroute0, iroute1)
    iroute2 = shortest_way.remote(Location[2], 5)
    inew_route2 = merge_route.remote(inew_route1, iroute2)
    iroute3 = shortest_way.remote(Location[3], 5)
    inew_route3 = merge_route.remote(inew_route2, iroute3)
    iroute4 = shortest_way.remote(Location[4], 5)
    inew_route4 = merge_route.remote(inew_route3, iroute4)
    iroute5 = shortest_way.remote(Location[4], 5)
    inew_route5 = merge_route.remote(inew_route4, iroute5)



    route = ray.get(new_route5)
    aroute = ray.get(anew_route5)
    broute = ray.get(bnew_route5)
    croute = ray.get(cnew_route5)
    droute = ray.get(dnew_route5)
    eroute = ray.get(enew_route5)
    froute = ray.get(fnew_route5)
    groute = ray.get(gnew_route5)
    hroute = ray.get(hnew_route5)
    iroute = ray.get(inew_route5)


    print(route)
    print(aroute)
    print(broute)
    print(croute)
    print(droute)
    print(eroute)
    print(froute)
    print(groute)
    print(hroute)
    print(iroute)



#time = timeit.timeit('fun()', 'from __main__ import fun', number=1)
#print("time =", time)

tracemalloc.start()
fun()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
tracemalloc.stop()