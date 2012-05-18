from __future__ import absolute_import
import os
from sanetime import time,delta,ndelta

get_pid = os.getpid

def get_parent_pid(from_pid=None):  # get parent pid
    if from_pid == 0: return 0
    if not from_pid: return os.getppid()
    return _get_parent_pid(from_pid)

def get_grandparent_pid(from_pid=None):  # get grandparent pid
    parent_pid = get_parent_pid(from_pid)
    if parent_pid ==0: return 0
    return _get_parent_pid(parent_pid)

def _get_parent_pid(pid):
    return int(os.popen('ps -p %d -oppid=' % pid).read().strip())
      
# alternative aliases using the ppp pattern in os:
getpid = get_pid
getppid = get_parent_pid
getpppid = get_grandparent_pid


class FileLock(object):
    def __init__(self, name, poll_rate=None, timeout=None): # poll_rate & timeout as deltas or micros
        super(FileLock, self).__init__()
        self.lock_dir = '%s.lock' % str(name)
        self.locked = False
        self.poll_rate = ndelta(poll_rate) or delta(ms=100)
        self.timeout = delta(timeout or 0)

    def __enter__(self): 
        self.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()

    def lock(self, poll_rate=None, timeout=None): # poll_rate & timeout as deltas or micros
        if timeout is None:
            timeout = delta(self.timeout)
        if poll_rate is None:
            poll_rate = delta(self.poll_rate)
            
        start = time()
        while not self._attempt_lock():
            self.poll_rate.sleep()
            if time() > start + timeout: 
                break
        return self.locked

    def unlock(self):
        if self.locked:
            os.rmdir(self.lock_dir)
            self.locked = False
        return not self.locked

    def _attempt_lock(self):
        try:
            os.mkdir(self.lock_dir)
            self.locked = True
        except OSError:
            self.locked = False
        return self.locked

