# build指令：
# docker build -t="UserName/ubuntu:Tag" .
# 其中 UserName 和 Tag 可更改， . 指在当前文件夹寻找 dockerfile

# 采用Ubuntu
FROM    ubuntu:latest
MAINTAINER      x_do_our_best

# 采用科大源
RUN  sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get clean & apt-get update
# Python3 安装
RUN apt-get -y install python3 python3-pip
# ray 等依赖安装
RUN pip3 install -U ray[default] -i https://pypi.tuna.tsinghua.edu.cn/simple
# 运行的源文件复制进文档中
COPY *.py /home/ray/

# 运行指令，可调整
CMD python3 /home/ray/ray_test_3.py

# 运行指令
# docker run -it UserName/ubuntu:Tag