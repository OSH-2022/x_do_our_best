# 导入ray，并初始化执行环境
import ray
ray.init()

# 定义ray remote函数
@ray.remote
def hello():
    return "Hello world !"

# 异步执行remote函数，返回结果id
object_id = hello.remote()

# 同步获取计算结果
hello = ray.get(object_id)

# 输出计算结果
print(hello)