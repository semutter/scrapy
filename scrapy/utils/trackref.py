"""This module provides some functions and classes to record and report
references to live object instances.

If you want live objects for a particular class to be tracked, you only have to
subclass form object_ref (instead of object).

About performance: This library has a minimal performance impact when enabled,
and no performance penalty at all when disabled (as object_ref becomes just an
alias to object in that case).
"""

from __future__ import print_function
import weakref, os
from collections import defaultdict
from time import time
from operator import itemgetter

NoneType = type(None)

#默认字典，每个key默认value为一个weakkeydictionary
live_refs = defaultdict(weakref.WeakKeyDictionary)

class object_ref(object):
    """Inherit from this class (instead of object) to a keep a record of live
    instances"""

    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        #继承自object的新式类才会有__new__
        #__new__至少有一个参数cls，代表要实例化的类，此参数在实例化时由python解释器自动提供
        #存在参数*args与**kwargs的作用是在多个继承中保持一致性
        obj = object.__new__(cls)
        live_refs[cls][obj] = time()
        return obj

def format_live_refs(ignore=NoneType):
    s = "Live References" + os.linesep + os.linesep
    now = time()
    for cls, wdict in live_refs.iteritems():
        if not wdict:
            continue
        if issubclass(cls, ignore):
            continue
        oldest = min(wdict.itervalues())
        s += "%-30s %6d   oldest: %ds ago" % (cls.__name__, len(wdict), \
            now-oldest) + os.linesep
    return s

def print_live_refs(*a, **kw):
    print(format_live_refs(*a, **kw))

def get_oldest(class_name):
    for cls, wdict in live_refs.iteritems():
        if cls.__name__ == class_name:
            if wdict:
                #按value值进行排序，找到最小的，亦即时间最小的，亦即最老的，
                #返回对应的key，即这个class_name下的最老的对象
                return min(wdict.iteritems(), key=itemgetter(1))[0]

def iter_all(class_name):
    for cls, wdict in live_refs.iteritems():
        if cls.__name__ == class_name:
            return wdict.iterkeys()
    #返回该class_name下的所有对象的迭代器
