from multiprocessing import (
    Process,
    Lock, RLock, Semaphore, Queue, Event, Condition, Barrier,
    Value, Array, Pipe, Manager
)
import logging
import multiprocessing
import time


logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

def worker1(i):
    logging.debug('start')
    logging.debug(i)
    logging.debug('end')

def worker2(i):
    logging.debug('start')
    logging.debug(i)
    logging.debug('end')

if __name__ == '__main__':
    i = 10
    p1 = multiprocessing.Process(name='p1', target=worker1, args=(i,))
    p1.daemon = True
    p2 = multiprocessing.Process(name='p2', target=worker2, args=(i,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
