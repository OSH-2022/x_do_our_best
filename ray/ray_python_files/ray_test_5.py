import ray
ray.init()

@ray.remote
def f(x):
    pass

x = "hello"

# 对象x往ObjectStore拷贝里10次
[f.remote(x) for _ in range(10)]

# 对象x仅往ObjectStore拷贝1次
x_id = ray.put(x)
[f.remote(x_id) for _ in range(10)]
