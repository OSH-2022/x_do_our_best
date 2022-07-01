import ray
import time,datetime
import profile
import cProfile

# Start Ray.
ray.init()

import numpy as np

# 定义两个远程函数。
# 这些函数的调用创建了远程执行的任务

@ray.remote
def create_matrix(size):
    return np.random.normal(size=size)
@ray.remote
def multiply_matrices(x, y):
    return np.dot(x, y)

@profile
def fun():
    result_ids = []
    for i in range(400):
        # 开始两个并行的任务，这些会立即返回futures并在后台执行
        x_id = create_matrix.remote([1000, 1000])
        print(datetime.datetime.now())
        y_id = create_matrix.remote([1000, 1000])
        print(datetime.datetime.now())
        # 开始第三个任务，但这并不会被提前计划，直到前两个任务都完成了.
        result_ids.append(multiply_matrices.remote(x_id, y_id))
        print(datetime.datetime.now())
    # 获取结果。这个结果直到第三个任务完成才能得到。只有get创建以后所有的任务才开始创建执行。
    z_id = ray.get(result_ids)
    print(z_id)

fun()
