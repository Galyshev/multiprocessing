import datetime
import queue
from threading import Thread
from multiprocessing import Process, Queue


# 9999 / 9999 => 99 999 999 (+1) => 100 000 000 (/4 = 25 000 000)
def luckyTicket(start, end):
    count = 0
    for i in range(start, end):
        line = str(i).rjust(8, '0')
        left = int(line[0]) + int(line[1]) + int(line[2]) + int(line[3])
        right = int(line[4]) + int(line[5]) + int(line[6]) + int(line[7])
        if left == right:
            count +=1
    print(count)

def luckyTicket_Queue(q_number,q_rezult):
    while True:
        try:
            q = q_number.get_nowait()
            line = str(q).rjust(4, '0')
            left = int(line[0]) + int(line[1])
            right = int(line[2]) + int(line[3])
        except queue.Empty:
            break
        else:
            if left == right:
                q_rezult.put(line)
    return True




def threadExample():
    t1 = Thread(target=luckyTicket, args=(0, 25000000))
    t2 = Thread(target=luckyTicket, args=(25000000, 50000000))
    t3 = Thread(target=luckyTicket, args=(50000000, 75000000))
    t4 = Thread(target=luckyTicket, args=(75000000, 100000000))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

def processExample():
    t1 = Process(target=luckyTicket, args=(0, 25000000))
    t2 = Process(target=luckyTicket, args=(25000000, 50000000))
    t3 = Process(target=luckyTicket, args=(50000000, 75000000))
    t4 = Process(target=luckyTicket, args=(75000000, 100000000))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

def processQueue():
    q_number = Queue()
    q_rezult = Queue()
    processes = []
    for i in range(10000):
        q_number.put(i)

    for tmp in range(4):    #4 - количество процессов
        p = Process(target=luckyTicket_Queue, args=(q_number, q_rezult))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(q_rezult.qsize())

    # для печати счастливых номеров
    # while not q_rezult.empty():
    #     print(q_rezult.get())


if __name__ == '__main__':
    # один поток
    start_time = datetime.datetime.now()
    luckyTicket(0, 100000000)
    time = datetime.datetime.now() - start_time
    print(f"для одного потока время расчета {time}")
    print("-------------------------------")

    # четыре потока
    start_time = datetime.datetime.now()
    threadExample()
    time = datetime.datetime.now() - start_time
    print(f"для четырех потоков время расчета {time}")
    print("-------------------------------")

    # четыре процесса
    start_time = datetime.datetime.now()
    processExample()
    time = datetime.datetime.now() - start_time
    print(f"для четырех проессов время расчета {time}")
    print("-------------------------------")

    # четыре процесса + очередь. Без замера времени, так как реализация для себя, проверить свои знания )
    processQueue()