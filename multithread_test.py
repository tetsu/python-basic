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

def counter():
    i = 1
    while True:
        yield i
        i = i + 1

if __name__ == '__main__':

    i  = counter()

    print('\n**** 1. test two threads ******\n')

    t1 = threading.Thread(name='thread{}'.format(i.__next__()), target=worker1)
    t2 = threading.Thread(
        name='thread{}'.format(i.__next__()),
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
            name='thread{}'.format(i.__next__()),
            target=worker1
        )
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

    print('\n***** 3. Using Daemon and Threading Enumerate *****\n')
    for _ in range(5):
        t = threading.Thread(
            name='thread{}'.format(i.__next__()),
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
    t.setName('thread{}'.format(i.__next__()))
    t.start()
    t.join()

    print('\n***** 5. Lock thread so that different thread won\'t interrupt *****\n')
    d = {'x': 0}
    lock = threading.Lock()
    t1 = threading.Thread(
        name='thread{}'.format(i.__next__()),
        target=worker3,
        args=(d, lock)
    )
    t2 = threading.Thread(
        name='thread{}'.format(i.__next__()),
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
        name='thread{}'.format(i.__next__()),
        target=worker3,
        args=(d, lock)
    )
    t2 = threading.Thread(
        name='thread{}'.format(i.__next__()),
        target=worker5,
        args=(d, lock)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('\n***** 7. with semaphore to start 2 locked threads first *****\n')
    semaphore = threading.Semaphore(2)
    t1 = threading.Thread(name='thread{}'.format(i.__next__()), target=worker6, args=(semaphore,))
    t2 = threading.Thread(name='thread{}'.format(i.__next__()), target=worker7, args=(semaphore,))
    t3 = threading.Thread(name='thread{}'.format(i.__next__()), target=worker8, args=(semaphore,))

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

    print('\n***** 8. control thread with queue *****\n')
    q = queue.Queue()
    t1 = threading.Thread(name='thread{}'.format(i.__next__()), target=worker9, args=(q,))
    t2 = threading.Thread(name='thread{}'.format(i.__next__()), target=worker10, args=(q,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('\n***** 9. control thread with queue *****\n')
    q = queue.Queue()
    for index in range(10):
        q.put(index)
    t1 = threading.Thread(name='thread{}'.format(i.__next__()), target=worker11, args=(q,))

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
    for _ in range(3):
        t = threading.Thread(name='thread{}'.format(i.__next__()), target=worker11, args=(q,))
        t.start()
        ts.append(t)
    logging.debug('tasks are not done')
    q.join()
    logging.debug('tasks are done')
    for _ in range(len(ts)):
        q.put(None)
    [t.join() for t in ts]
