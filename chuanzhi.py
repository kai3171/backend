import multiprocessing
import os
import signal

parent_conn, child_conn = multiprocessing.Pipe()
def process_function(id,start, end, envet, queua,queub):
    for i in range(start, end+1):
        print(id,'working:',i)
        print('pid:',os.getpid())
        if i == 200:
            queua.put(i)
            queub.put(os.getpid())
            envet.set()

# 创建进程对象
envett = multiprocessing.Event()
queues = [multiprocessing.Queue() for i in range(50)]
myqueue =  multiprocessing.Queue()
myqueueb =  multiprocessing.Queue()
process_1 = multiprocessing.Process(target=process_function, args=(1,1, 2500,envett,queues[0],queues[1]))
# 启动进程
process_1.start()
pid_using = queues[1].get()
os.kill(pid_using,signal.SIGTERM)
print('父进程pid为：',os.getpid())
print('子进程pid为:',pid_using)
print('子进程传值为:',queues[0].get())
print('进程顺利结束')

