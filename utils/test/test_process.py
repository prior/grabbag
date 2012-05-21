import unittest, shutil, os
from ..process import get_pid, get_parent_pid, get_grandparent_pid, get_children_pids, Process, ProcessTree, ProcessSlotLock
import multiprocessing as mp


BREADTH = 2
SLOT_DIR = '_slots'

def subsubprocess(qin, qout):
    while True:
        command = qin.get()
#        print "subsub: %s (%s)" % (command, get_pid())
        if command == 'QUIT': 
            return
        elif command == 'GET_PID': 
            qout.put(get_pid())
        elif command == 'GET_SLOT': 
            slot_lock = ProcessSlotLock(SLOT_DIR, 2, BREADTH)
            slot = slot_lock.slot
#            print "subsub: %s (%s) [slot=%s]" % (command, get_pid(), slot)
            qout.put(slot)

def subprocess(qin, qout):
    qouts = []
    qins = []
    processes = []
    for i in range(BREADTH):
        _qin, _qout = mp.Queue(), mp.Queue()
        p = mp.Process(target=subsubprocess, args=(_qout,_qin))
        p.start()
        processes.append(p)
        qouts.append(_qout)
        qins.append(_qin)

    while True:
        command = qin.get()
#        print "sub: %s (%s)" % (command, get_pid())
        if command == 'QUIT':
            for qo in qouts: qo.put('QUIT')
            for p in processes: p.join()
            return
        elif command == 'GET_PIDS':
            for qo in qouts: qo.put('GET_PID')
            child_pids = []
            for qi in qins: child_pids.append(qi.get())
            qout.put((get_pid(),tuple(child_pids)))
        elif command == 'GET_SLOTS':
            for qo in qouts: qo.put('GET_SLOT')
            slots = []
            for qi in qins: slots.append(qi.get())
            qout.put(tuple(slots))


class ProcessTest(unittest.TestCase):

    @classmethod
    def setUpClass(kls):
        kls.qouts = []
        kls.qins = []
        kls.processes = []
        kls.children_pids = {}
        kls.grandchildren_pids = ()
        for i in range(BREADTH):
            qin,qout = mp.Queue(), mp.Queue()
            p = mp.Process(target=subprocess, args=(qout,qin))
            p.start()
            kls.processes.append(p)
            kls.qouts.append(qout)
            kls.qins.append(qin)
            qout.put('GET_PIDS')
        for qin in kls.qins:
            child_pid, grandchildren_pids = qin.get()
            kls.children_pids[child_pid] = grandchildren_pids
            kls.grandchildren_pids += grandchildren_pids

    @classmethod
    def tearDownClass(kls):
        for qout in kls.qouts:
            qout.put('QUIT')
        for p in kls.processes:
            p.join()
        kls._clear_slot_dir()

    def setUp(self): self._clear_slot_dir()
    def tearDown(self): self._clear_slot_dir()

    @classmethod
    def _clear_slot_dir(kls):
        try:
            shutil.rmtree(SLOT_DIR)
        except OSError:
            pass

    def test_setup(self):
        self.assertEquals(BREADTH**2+BREADTH+1, len(set((get_pid(),) + tuple(self.children_pids.keys()) + self.grandchildren_pids)))

    def test_parent_pid(self):
        for pid, child_pids in self.children_pids.items():
            self.assertEquals(get_pid(), get_parent_pid(pid))
            for grandchild_pid in self.children_pids[pid]:
                self.assertEquals(pid, get_parent_pid(grandchild_pid))

    def test_grandparent_pid(self):
        for pid in self.grandchildren_pids:
            self.assertEquals(get_pid(), get_grandparent_pid(pid))

    def test_children_pids(self):
        self.assertEquals(set(self.children_pids.keys()), set(get_children_pids()))
        for pid,child_pids in self.children_pids.items():
            self.assertEquals(set(child_pids), set(get_children_pids(pid)))

    def test_process_parent(self):
        for pid, child_pids in self.children_pids.items():
            self.assertEquals(Process(), Process(pid).parent)
            for grandchild_pid in self.children_pids[pid]:
                self.assertEquals(Process(pid), Process(grandchild_pid).parent)
                self.assertNotEquals(Process(), Process(grandchild_pid).parent)

    def test_process_grandparent(self):
        for pid in self.grandchildren_pids:
            self.assertEquals(Process(), Process(pid).parent.parent)

    def test_process_children(self):
        self.assertEquals(set([Process(pid) for pid in self.children_pids.keys()]), set(Process().children))
        for pid,child_pids in self.children_pids.items():
            self.assertEquals(set([Process(p) for p in child_pids]), set(Process(pid).children))

    def test_process_tree(self):
        pt = ProcessTree(ascendant_depth=0, descendant_depth=0)
        self.assertNotIn(get_grandparent_pid(), pt)
        self.assertNotIn(get_parent_pid(), pt)
        self.assertIn(get_pid(), pt)
        for pid, child_pids in self.children_pids.items():
            self.assertNotIn(pid, pt)
            for cpid in child_pids:
                self.assertNotIn(cpid, pt)

        pt = ProcessTree(ascendant_depth=0, descendant_depth=1)
        self.assertNotIn(get_grandparent_pid(), pt)
        self.assertNotIn(get_parent_pid(), pt)
        self.assertIn(get_pid(), pt)
        for pid, child_pids in self.children_pids.items():
            self.assertIn(pid, pt)
            for cpid in child_pids:
                self.assertNotIn(cpid, pt)

        pt = ProcessTree(ascendant_depth=1, descendant_depth=0)
        self.assertNotIn(get_grandparent_pid(), pt)
        self.assertIn(get_parent_pid(), pt)
        self.assertIn(get_pid(), pt)
        for pid, child_pids in self.children_pids.items():
            self.assertNotIn(pid, pt)
            for cpid in child_pids:
                self.assertNotIn(cpid, pt)

        pt = ProcessTree(ascendant_depth=1)
        self.assertNotIn(get_grandparent_pid(), pt)
        self.assertIn(get_parent_pid(), pt)
        self.assertIn(get_pid(), pt)
        for pid, child_pids in self.children_pids.items():
            self.assertIn(pid, pt)
            for cpid in child_pids:
                self.assertIn(cpid, pt)

        pt = ProcessTree(anchor_process = self.grandchildren_pids[0], ascendant_depth=2)
        self.assertEquals(BREADTH**2+BREADTH+1, len(pt.pool))
        self.assertNotIn(get_grandparent_pid(), pt)
        self.assertNotIn(get_parent_pid(), pt)
        self.assertIn(get_pid(), pt)
        for pid, child_pids in self.children_pids.items():
            self.assertIn(pid, pt)
            for cpid in child_pids:
                self.assertIn(cpid, pt)

        pt = ProcessTree(anchor_process = self.grandchildren_pids[0], ascendant_depth=1)
        self.assertEquals(BREADTH+1, len(pt.pool))
        self.assertNotIn(get_grandparent_pid(), pt)
        self.assertNotIn(get_parent_pid(), pt)
        self.assertNotIn(get_pid(), pt)
        for pid, child_pids in self.children_pids.items():
            in_ecosystem = self.grandchildren_pids[0] in child_pids
            if in_ecosystem:
                self.assertIn(pid, pt)
                for cpid in child_pids:
                    self.assertIn(cpid, pt)
            else:
                self.assertNotIn(pid, pt)
                for cpid in child_pids:
                    self.assertNotIn(cpid, pt)

    def test_slot_lock(self):
        for qout in self.qouts:
            qout.put('GET_SLOTS')
        slots = ()
        for qin in self.qins:
            slots += qin.get()
        self.assertEquals(BREADTH**2, len(set(slots)))
        self.assertEquals(BREADTH**2, len([filename for filename in os.listdir('_slots') if filename.endswith('.pid')]))
        for qout in self.qouts:
            qout.put('GET_SLOTS')
        slots2 = ()
        for qin in self.qins:
            slots2 += qin.get()
        self.assertEquals(set(slots),set(slots2))




