import logging
import queue
import threading
import time


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def worker1():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

def worker2(x, y=1):
    logging.debug('start')
    logging.debug(x)
    time.sleep(1)
    logging.debug(y)
    logging.debug('end')

def worker3(d, lock):
    logging.debug('start')
    lock.acquire()
    i = d['x']
    time.sleep(1)
    d['x'] = i + 1
    logging.debug(d)
    lock.release()
    logging.debug('end')

def worker4(d, lock):
    logging.debug('start')
    with lock:
        i = d['x']
        d['x'] = i + 1
        logging.debug(d)
    logging.debug('end')

def worker5(d, lock):
    logging.debug('start')
    with lock:
        i = d['x']
        d['x'] = i + 1
        logging.debug(d)
        with lock:
            d['x'] = i + 1
    logging.debug('end')

def worker6(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def worker7(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def worker8(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def worker9(queue):
    logging.debug('start')
    queue.put(100)
    time.sleep(3)
    queue.put(200)
    logging.debug('end')

def worker10(queue):
    logging.debug('start')
    logging.debug(queue.get())
    logging.debug(queue.get())
    logging.debug('end')

def worker11(queue):
    logging.debug('start')
    while True:
        item = queue.get()
        if item is None:
            break;
        logging.debug(item)
        queue.task_done()
    logging.debug('end')

def worker11_1(event):
    event.wait() # wait until event starts
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

def worker11_2(event):
    event.wait() # wait until event starts
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

def worker11_3(event):
    logging.debug('start')
    logging.debug('end')
    event.set() # event starts here

def worker12_1(condition):
    with condition:
        condition.wait() # wait until condition gets notified
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def worker12_2(condition):
    with condition:
        condition.wait() # wait until prefios condition ends
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def worker12_3(condition):
    with condition:
        logging.debug('start')
        logging.debug('end')
        condition.notifyAll() # conditions get notified here

def worker13_1(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def worker13_2(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def counter():
    i = 1
    while True:
        yield i
        i = i + 1

if __name__ == '__main__':

    i  = counter()

    print('\n**** 1. test two threads ******\n')

    t1 = threading.Thread(name='thread1_1', target=worker1)
    t2 = threading.Thread(
        name='thread1_2',
        target=worker2,
        args=(100, ),
        kwargs={'y': 200}
    )
    t1.start()
    t2.start()
    print('started')
    t1.join()
    t2.join()


    print('\n**** 2. thread with for-loop and daemon ******\n')
    threads = []
    for _ in range(5):
        t = threading.Thread(
            name='thread2',
            target=worker1
        )
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()


    print('\n***** 3. Using Daemon and Threading Enumerate *****\n')
    for index, _ in enumerate(range(5)):
        t = threading.Thread(
            name='thread3_{}'.format(index + 1),
            target=worker1
        )
        t.setDaemon(True)
        t.start()
    for thread in threading.enumerate():
        if thread is threading.currentThread():
            print(thread)
            continue
        thread.join()

    print('\n***** 4. Using Threading Timer *****\n')
    t = threading.Timer(3, worker2, args=(100,), kwargs={'y': 200})
    t.setName('thread4')
    t.start()
    t.join()


    print('\n***** 5. Lock thread so that different thread won\'t interrupt *****\n')
    d = {'x': 0}
    lock = threading.Lock()
    t1 = threading.Thread(
        name='thread5_1',
        target=worker3,
        args=(d, lock)
    )
    t2 = threading.Thread(
        name='thread5_2',
        target=worker4,
        args=(d, lock)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()


    print('\n***** 6. RLock thread to acquire a lock within a lock *****\n')
    d = {'x': 0}
    lock = threading.RLock()
    t1 = threading.Thread(
        name='thread6_1',
        target=worker3,
        args=(d, lock)
    )
    t2 = threading.Thread(
        name='thread6_2',
        target=worker5,
        args=(d, lock)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()


    print('\n***** 7. with semaphore to start 2 locked threads first *****\n')
    semaphore = threading.Semaphore(2)
    t1 = threading.Thread(name='thread7_1', target=worker6, args=(semaphore,))
    t2 = threading.Thread(name='thread7_2', target=worker7, args=(semaphore,))
    t3 = threading.Thread(name='thread7_3', target=worker8, args=(semaphore,))

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


    print('\n***** 8. control thread with queue *****\n')
    q = queue.Queue()
    t1 = threading.Thread(name='thread8_1', target=worker9, args=(q,))
    t2 = threading.Thread(name='thread8_2', target=worker10, args=(q,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('\n***** 9. control thread with queue *****\n')
    q = queue.Queue()
    for index in range(10):
        q.put(index)
    t1 = threading.Thread(name='thread9_1', target=worker11, args=(q,))

    t1.start()
    logging.debug('tasks are not done')
    q.join()
    logging.debug('tasks are done')
    q.put(None)
    t1.join()


    print('\n***** 10. queue with simultaniously running threads *****\n')
    q = queue.Queue()
    for index in range(100):
        q.put(index)
    ts = []
    for index, _ in enumerate(range(3)):
        t = threading.Thread(name='thread10_{}'.format(index + 1), target=worker11, args=(q,))
        t.start()
        ts.append(t)
    logging.debug('tasks are not done')
    q.join()
    logging.debug('tasks are done')
    for _ in range(len(ts)):
        q.put(None)
    [t.join() for t in ts]


    print('\n***** 11. Using Event *****\n')
    event = threading.Event()
    t1 = threading.Thread(
        name='thread11_1',
        target=worker11_1,
        args=(event,)
    )
    t2 = threading.Thread(
        name='thread11_2',
        target=worker11_2,
        args=(event,)
    )
    t3 = threading.Thread(
        name='thread11_3',
        target=worker11_3,
        args=(event,)
    )
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


    print('\n***** 12. Using Condition *****\n')
    condition = threading.Condition()
    t1 = threading.Thread(
        name='thread12_1',
        target=worker12_1,
        args=(condition,)
    )
    t2 = threading.Thread(
        name='thread12_2',
        target=worker12_2,
        args=(condition,)
    )
    t3 = threading.Thread(
        name='thread12_3',
        target=worker12_3,
        args=(condition,)
    )
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


    print('\n***** 13. Using Barrier *****\n')
    barrier = threading.Barrier(2)
    t1 = threading.Thread(
        name='thread13_1',
        target=worker13_1,
        args=(barrier,)
    )
    t2 = threading.Thread(
        name='thread13_2',
        target=worker13_2,
        args=(barrier,)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()
