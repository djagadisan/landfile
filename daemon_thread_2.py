import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s'
                    )


def daemon():
    logging.debug('Starting')
    time.sleep(20)
    logging.debug('Exiting')

d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)


def non_daemon():
    logging.debug('Starting')
    for i in range(30):
        time.sleep(1)
        logging.debug(i)
    logging.debug('Exiting')

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()



d.join()
t.join()
print d.isAlive()
print t.isAlive()