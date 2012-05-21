from __future__ import absolute_import
import os,re
from sanetime import ndelta
from . import os as _os
from .property import cached_property


PS_LISTING_COMMAND = 'ps -ax -opid= -oppid= -oargs='
PS_LISTING_PATTERN = re.compile("^\s*(\d+)\s+(\d+)\s+(.*)\s*$")

get_pid = os.getpid
def get_parent_pid(from_pid=None):  # get parent pid
    if from_pid is None: return os.getppid()
    if from_pid <= 1: return 0
    return _get_parent_pid(from_pid)

def get_grandparent_pid(from_pid=None):  # get grandparent pid
    parent_pid = get_parent_pid(from_pid)
    if parent_pid <= 1: return 0
    return _get_parent_pid(parent_pid)

def _get_parent_pid(pid):  # slow! (2ms runtime)
    return int(os.popen('ps -p %d -oppid=' % pid).read().strip())

def get_children_pids(from_pid=None):  # slow! (2ms runtime)
    if from_pid is None: 
        from_pid = get_pid()
    children = []
    lines = os.popen(PS_LISTING_COMMAND).read().strip().split('\n')
    for line in lines:
        _pid, _ppid, _command = re.match(PS_LISTING_PATTERN, line).group(1,2,3)
        if int(_ppid) == from_pid and _command != PS_LISTING_COMMAND:
            children.append(int(_pid))
    return tuple(children)


# alternative aliases using the ppp pattern in os:
getpid = get_pid
getppid = get_parent_pid
getpppid = get_grandparent_pid

_os.getpid = getpid
_os.getppid = getppid
_os.getpppid = getpppid



class Process(object):
    def __init__(self, pid=None):
        if isinstance(pid, self.__class__):
            self.pid = pid.pid
            self.this_process = pid.this_process
        elif pid is None:
            self.pid = get_pid()
            self.this_process = True
        else:
            self.pid = pid
            self.this_process = False

    @cached_property
    def parent(self):
        if self.pid <= 1: return None
        return Process(get_parent_pid(from_pid = None if self.this_process else self.pid))

    @cached_property
    def children(self):
        return [Process(pid) for pid in get_children_pids(self.pid)]

    def __cmp__(self, other): return cmp(self.pid, int(other))
    def __hash__(self): return self.pid.__hash__()
    def __int__(self): return self.pid
    def __long__(self): return long(self.pid)


class ProcessTree(object):
    def __init__(self, anchor_process=None, ascendant_depth=None, descendant_depth=None):
        self.anchor_process = Process(anchor_process)
        self.ascendant_depth = ascendant_depth
        self.descendant_depth = descendant_depth
        self._build()

    def _build(self):
        ascendants = {}
        descendants = {}
        lines = os.popen(PS_LISTING_COMMAND).read().strip().split('\n')
        for line in lines:
            _pid, _ppid, command = re.match(PS_LISTING_PATTERN, line).group(1,2,3)
            pid = int(_pid)
            ppid = int(_ppid)
            if command != PS_LISTING_COMMAND:
                descendants.setdefault(ppid,[]).append(pid)
                ascendants[pid] = ppid

        # find top edge
        top_pid = self.anchor_process.pid
        ancestor_count = 0
        while (self.ascendant_depth is not None and ancestor_count < self.ascendant_depth or self.ascendant_depth is None) and top_pid > 1:
            top_pid = ascendants[top_pid]
            ancestor_count += 1

        # find bottom limit
        depth_limit = None
        if self.descendant_depth is not None:
            depth_limit = ancestor_count + self.descendant_depth

        # build out tree
        self.origin = self.anchor_process if self.anchor_process.pid==top_pid else Process(top_pid)
        self.pool = set([self.origin])
        self._build_children_processes(self.origin, descendants, depth_limit)

    def _build_children_processes(self, node, descendants, depth_limit):
        if depth_limit is not None and depth_limit <= 0: 
            return node
        node.children = []
        for pid in descendants.get(node.pid,[]):
            process = self.anchor_process if self.anchor_process.pid==pid else Process(pid)
            process.parent = node
            self._build_children_processes(process, descendants, None if depth_limit is None else depth_limit-1)
            self.pool.add(process)
            node.children.append(process)
        return node

    def __contains__(self, item): return item in self.pool



# locks a process down to a distinct ordinal slot in a given pid ecosystem
class ProcessSlotLock(object):
    def __init__(self, slot_dir, ascendant_depth=1, process_breadth=None):  # generally 5ms times the number of processes you gotta deal with 
        self.slot_dir = slot_dir
        self.ascendant_depth = ascendant_depth
        self.slot_takeover_timeout = ndelta(ms=(process_breadth or 20)*50)

    @cached_property
    def slot(self):
        try:
            os.mkdir(self.slot_dir)
        except OSError:
            pass

        slot = 1
        while True:
            try:
                with _os.FileLock("%s/%s" % (self.slot_dir, slot), timeout=self.slot_takeover_timeout):
                    if self._attempt_slot_takeover(slot):
                        break
            except _os.FileLockError:
                pass
            slot+=1
        return slot

    def _attempt_slot_takeover(self, slot):
        pid_file = '%s/%s.pid' % (self.slot_dir, slot)
        pid = None
        try: 
            with open(pid_file,'r') as f:
                pid = int(f.read().strip())
        except BaseException:
            pass

        if pid:
            if pid == get_pid():
                return True
            pt = ProcessTree(ascendant_depth = self.ascendant_depth)
            if pid in pt:
                return False
        with open(pid_file,'w') as f:
            f.write(str(get_pid()) + "\n")
        return True


















#class Rodanable(object):
    #""" A mixin to simplify python rodan usage even more. """

    #def __init__(self, family=None, cluster_type=None, cluster_name='django', service_type=None, env=None, process_distinction_ascendant_depth=None):
        #super(RodanClient, self).__init__()
        #self._family = family or '?'
        #self._cluster_type = cluster_type or '?'
        #self._cluster_name = cluster_name or '?'
        #self._service_type = service_type or '?'
        #self._env = env or (globals().get('settings',None) and settings.ENV)
        #self._hostname = os.popen('hostname').read().strip().split('.')[:1]
        #if process_distinction_ascendant_depth is not None:
            #self._hostname = "%s-%02d" % (self._hostname, ProcessSlotLock('_rodan',process_distinction_ascendant_depth,delta(ms=100)).slot)
        #self._base_payload = {
            #'family': self._family,
            #'cluster_type': self._cluster_type,
            #'cluster_name': self._cluster_name,
            #'service_type': self._service_type,
            #'env': self._env or setting,
            #'hostname': self._hostname }

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
            #If you're inheriting this class, you need to inherit and override this function to reset the stats you care about
        #""")


