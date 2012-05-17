from __future__ import absolute_import
import os

get_pid = os.getpid

def _get_parent_pid(pid):
    return int(os.popen('ps -p %d -oppid=' % pid).read().strip())

def get_parent_pid(from_pid=None):  # get parent pid
    if from_pid == 0: return 0
    if not from_pid: return os.getppid()
    return _get_parent_pid(from_pid)

def get_grandparent_pid(from_pid=None):  # get grandparent pid
    parent_pid = get_parent_pid(from_pid)
    if parent_pid ==0: return 0
    return _get_parent_pid(parent_pid)
      
# alternative aliases using the ppp pattern in os:
getpid = get_pid
getppid = get_parent_pid
getpppid = get_grandparent_pid

