from multiprocessing import Process
import time
import os

def loop_a():
    for i in range(1,1000000):
        pass
    print(type(os.getpid()))

def loop_b():
    for i in range(1,1000000):
        pass
    print(time.time())
    print(type(os.getpid()))

if __name__ == '__main__':
    print(time.time())
    Process(target=loop_a).start()
    Process(target=loop_b).start()
