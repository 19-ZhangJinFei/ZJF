# 线程，进程
# 进程是一个资源单位，线程是一个执行单位
# 进程里面包括一个或多个线程，每一个进程至少要有一个线程
# 启动每一个程序默认会有以一个主线程
# 单线程，一行一行执行
"""
def func():
    for i in range(1000):
        print("func",i)

if __name__ == '__main__':
    func()
    for i in range(1000):
        print("main",i)
"""

# 多线程的第一套写法
"""
from threading import Thread  # 线程类


def func():
    for i in range(1000):
        print("func", i)


if __name__ == '__main__':
    t = Thread(target=func)  # 创建线程并给线程安排任务
    t.start()  # 多线程状态为可以开始工作状态，具体的执行时间由cpu决定

    for i in range(1000):
        print('main', i)
"""


# 多线程的第二套写法
from threading import Thread
class MyThread(Thread):  # 继承
    def run(self):  # run是固定的 -> 当线程可以执行之后，被执行的就是run()
        for i in range(1000):
            print("子线程", i)


if __name__ == '__main__':
    t = MyThread()
    # t.run() 这是方法的调用了，不是单线程
    t.start()  # 开启线程
    for i in range(1000):
        print("主线程", i)