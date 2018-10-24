import logging
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

def counter():
    i = 1
    while True:
        yield i
        i = i + 1

if __name__ == '__main__':

    i  = counter()
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

    print('\n**********\n')
    # Using Daemon
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

    print('\n**********\n')
    # Using Daemon and Threading Enumerate
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

    print('\n**********\n')
    # Using Threading Timer
    t = threading.Timer(3, worker2, args=(100,), kwargs={'y': 200})
    t.setName('thread{}'.format(i.__next__()))
    t.start()
    t.join()

    print('\n**********\n')
    # Lock thread so that different thread won't interrupt
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

    print('\n**********\n')
    # Lock thread to acquire lock within lock
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
