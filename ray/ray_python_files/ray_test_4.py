import ray

ray.init()

@ray.remote
def A():
    return "A"

@ray.remote
def B():
    return "B"

@ray.remote
def C(a, b):
    return "C"

a_id = A.remote()
b_id = B.remote()
c_id = C.remote(a_id, b_id)
print(ray.get(c_id))