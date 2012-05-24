from __future__ import absolute_import
import os
from sanetime import time,delta,ndelta


class FileLock(object):
    def __init__(self, name, timeout=None, poll_rate=None): # poll_rate & timeout as deltas or micros
        super(FileLock, self).__init__()
        self.lock_dir = '%s.lock' % str(name)
        self.locked = False
        self.poll_rate = ndelta(poll_rate)
        self.timeout = ndelta(timeout)

    def __enter__(self):
        if not self.lock():
            raise FileLockError("Unable to Lock")
        return self

    def __exit__(self, type, value, traceback):
        self.unlock()

    def lock(self, timeout=None, poll_rate=None): # poll_rate & timeout as deltas or micros
        timeout = ndelta(timeout) or self.timeout or delta(0)
        poll_rate = ndelta(poll_rate) or self.poll_rate
        start = time()
        while not self._attempt_lock():
            if poll_rate:
                poll_rate.sleep()
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

class FileLockError(Exception):
    pass

## locks a process down to a distinct ordinal slot in a given pid ecosystem
#class ProcessSlotLock(object):
    #def __init__(self, lock_dir, ancestry_depth=1, slot_takeover_timeout=None):  # generally 5ms times the number of processes you gotta deal with 
        #self.lock_dir = lock_dir
        #self.ancestry_depth = ancestry_depth
        #slot_takeover_timeout = ndelta(slot_takeover_timeout or 0)

    #@cached_property
    #def slot(self):
        #try:
            #os.mkdir(lock_dir)
        #except OSError:
            #pass

        #slot = 1
        #while True:
            #with FileLock("%s/%s" % (lock_dir, slot), timeout=self.slot_takeover_timeout):
                #if self._attempt_slot_takeover(slot):
                    #break
            #slot+=1
        #return slot

    #@cached_property
    #def _caring_pids(self):
        #caring = (xos.get_pid())
        #if self._ancestry_depth > 1:
            #for i in range(self._ancestry_depth - 1):
                #parent_pid = xos.get_parent_pid(None if i==0 else caring[-1]) # user the faster native stuff for speed when possible
                #if parent_pid > 1: caring_pids += (xos.get_parent_pid())
        #return set(caring)




    #def _attempt_slot_takeover(self, slot):
        #pid_file = '%s/%s.%s.pid' % (PROCESS_SLOT_DIR, self._type_digest, slot)
        #if os.path.exists(pid_file):
            #caring_pids = (xos.get_pid())
            #if self._process_distinction_depth > 0:
                #caring_pids += (xos.get_parent_pid())
            #if self._process_distinction_depth > 1:
                #for i in range(self._process_distinction_depth - 1):
                    #parent_pid = xos.get_parent_pid(
                    #caring_pids += (xos.get_parent_pid(

                #while (

                #caring_pids += (xos.get_grandparent_pid())
            #if self._process_distinction_depth > 2:

            #for x

            #for depth in xrange(self._process_distinction_depth):
                #caring_pids += (xos.get_pid(caring_pids[-1]),)
            #ecosystem_pids = [p.pid for p in psutil.get_process_list() if p.pid in caring_pids or p.ppid in caring_pids]
            #try: 
                #with open(pid_file,'r') as f:
                    #pid = int(f.read())
            #except BaseException:
                #pid = None
            #if pid in ecosystem_pids:
                #return False
        #with open(pid_file,'w') as f:
            #f.write(str(os.getppid()))
        #return True





#class Rodanable(object):
    #""" A mixin to simplify python rodan usage even more. """

    #def __init__(self, family=None, cluster_type=None, cluster_name='django', service_type=None, env=None, process_distinction_depth=None):
        ## process_distinction if specified is the ancestry depth over which to ensure uniqueness -- 
        ##   an ancestry depth of 0 doesn't really make sense
        ##   an ancestry depth of 1 means that no slot is taken if it is already taken by a sister process
        ##   an ancestry depth of 2 means that no slot is taken if it is already taken by a cousin or sister process
        ##   and so on..
        #super(RodanClient, self).__init__()
        #self._family = family or '?'
        #self._cluster_type = cluster_type or '?'
        #self._cluster_name = cluster_name or '?'
        #self._service_type = service_type or '?'
        #self._env = env or (globals().get('settings',None) and settings.ENV)
        #self._hostname = os.popen('hostname').read().strip().split('.')[:1]
        #self._process_distinction_depth = process_distinction_depth
        #if self._process_distinction_depth is not None:
            #self._hostname = "%s-%02d" % (self._hostname, self._process_slot)
        #self._base_payload = {
            #'family': self._family,
            #'cluster_type': self._cluster_type,
            #'cluster_name': self._cluster_name,
            #'service_type': self._service_type,
            #'env': self._env or setting,
            #'hostname': self._hostname }

    #@property
    #def _type_digest(self):
        #hashlib.md5("%s-%s-%s-%s-%s-%s"%(self._family, self._cluster_type, self._cluster_name, self._service_type, self._env, self._hostname)).hex_digest

    #@cached_property
    #def _process_slot(self):
        #try:
            #os.mkdir(PROCESS_SLOT_DIR)
        #except OSError:
            #pass

        #slot = 1
        #while True:
            #with FileLock("%s/%s.%s" % (PROCESS_SLOT_DIR, self._type_digest, slot), timeout=delta(s=5)):
                #if self._attempt_slot_takeover(slot):
                    #break
            #slot+=1
        #return slot

    #@cached_property
    #def _caring_pids(self):
        #caring = (xos.get_pid())
        #if self._process_distinction_depth > 1:
            #for i in range(self._process_distinction_depth - 1):
                #parent_pid = xos.get_parent_pid(caring[-1])
                #if parent_pid > 1: caring_pids += (xos.get_parent_pid())
        #return set(caring)




    #def _attempt_slot_takeover(self, slot):
        #pid_file = '%s/%s.%s.pid' % (PROCESS_SLOT_DIR, self._type_digest, slot)
        #if os.path.exists(pid_file):
            #caring_pids = (xos.get_pid())
            #if self._process_distinction_depth > 0:
                #caring_pids += (xos.get_parent_pid())
            #if self._process_distinction_depth > 1:
                #for i in range(self._process_distinction_depth - 1):
                    #parent_pid = xos.get_parent_pid(
                    #caring_pids += (xos.get_parent_pid(

                #while (

                #caring_pids += (xos.get_grandparent_pid())
            #if self._process_distinction_depth > 2:

            #for x

            #for depth in xrange(self._process_distinction_depth):
                #caring_pids += (xos.get_pid(caring_pids[-1]),)
            #ecosystem_pids = [p.pid for p in psutil.get_process_list() if p.pid in caring_pids or p.ppid in caring_pids]
            #try: 
                #with open(pid_file,'r') as f:
                    #pid = int(f.read())
            #except BaseException:
                #pid = None
            #if pid in ecosystem_pids:
                #return False
        #with open(pid_file,'w') as f:
            #f.write(str(os.getppid()))
        #return True



    #def _to_rodan(self, data):
        #response = requests.post("http://rodanapp.appspot.com/log",json.dumps(self._stats_payload))
        #return response.status_code>=200 and response.status_code<300

    #def push(self):
        #data = {
            #'family': self.family,
            #'cluster_type': self.cluster_type,
            #'service_type': self.service_type
        #now = time()
        #request_rate = self.requests/(now - self.reset_at).float_seconds
        #client_errors_percent = server_errors_percent = 0
        #if self.responses:
            #client_errors_percent = int((self.client_errors*100+0.5)/self.responses)
            #server_errors_percent = int((self.server_errors*100+0.5)/self.responses)
        #mean_timing_ms = None
        #if len(self.timings):
            #mean_timing_ms = delta(sum(self.timings)/len(self.timings)).ms
        #uptime = now - self.initialized_at
        #data = {}
        #data.update(self.base_payload)
        #items = data['data'] = []
        #items.append({'name':'requests', 'value':self.requests, 'display':"%0.1f/s (%s)"%(request_rate,self.requests)})
        #items.append({'name':'client errors', 'value':self.client_errors, 'display':"%s%% (%s)"%(client_errors_percent, self.client_errors)})
        #items.append({'name':'server errors', 'value':self.server_errors, 'display':"%s%% (%s)"%(server_errors_percent, self.server_errors)})
        #if mean_timing_ms:
            #items.append({'name':'response time', 'value':mean_timing_ms, 'display':"%sms"%mean_timing_ms})
        #items.append({'name':'uptime', 'value':uptime.seconds, 'display':"%dd, %02d:%02d:%02d"%(uptime.wmd, uptime.ph, uptime.pm, uptime.prs)})

        #self._rodan_snapshot
        #self._rodan_reset

    #def _rodan_reset(self):
        #raise NotImplementedError("""
            #If you're inheriting this class, you need to inherit and override this function to reset the stats you care about
        #""")

    #@property
    #def _rodan_snapshot(self):
        #raise NotImplementedError("""

