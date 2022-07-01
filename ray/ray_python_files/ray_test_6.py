import ray
ray.init()

@ray.remote(num_return_vals=2)
def f():
    return 1, 2

x_id, y_id = f.remote()
ray.get(x_id)  # 1
ray.get(y_id)  # 2