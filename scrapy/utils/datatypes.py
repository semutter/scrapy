"""
This module contains data types used by Scrapy which are not included in the
Python Standard Library.

This module must not depend on any module outside the Standard Library.
"""

import copy
from collections import OrderedDict


class MultiValueDictKeyError(KeyError):
    pass

class MultiValueDict(dict):
    """
    A subclass of dictionary customized to handle multiple values for the same key.

    >>> d = MultiValueDict({'name': ['Adrian', 'Simon'], 'position': ['Developer']})
    >>> d['name']
    'Simon'
    >>> d.getlist('name')
    ['Adrian', 'Simon']
    >>> d.get('lastname', 'nonexistent')
    'nonexistent'
    >>> d.setlist('lastname', ['Holovaty', 'Willison'])

    This class exists to solve the irritating problem raised by cgi.parse_qs,
    which returns a list for every key, even though most Web forms submit
    single name-value pairs.
    """
    #这个类存在的目的是为了解决由于cgi.parse_qs对于每一个key均返回一个list的情况，
    #尽管大部分网页表格提交单值对
    def __init__(self, key_to_list_mapping=()):
        dict.__init__(self, key_to_list_mapping)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, dict.__repr__(self))

    def __getitem__(self, key):
        """
        Returns the last data value for this key, or [] if it's an empty list;
        raises KeyError if not found.
        """
        #第一个try except不变，第二个可以变成
        #return list_[-1] if list_ else []
        try:
            list_ = dict.__getitem__(self, key)
        except KeyError:
            raise MultiValueDictKeyError("Key %r not found in %r" % (key, self))
        try:
            return list_[-1]
        except IndexError:
            return []

    def __setitem__(self, key, value):
        #只能设置单值value么，why
        dict.__setitem__(self, key, [value])

    def __copy__(self):
        #返回当前对象的所有的items重新构造出来的一个对象
        #self.__class__很神奇
        return self.__class__(dict.items(self))

    def __deepcopy__(self, memo=None):
        #python 标准库中的dict是否也有memo这个对象
        #下面的代码说明也有，memo作用？？
        #copy的代码学习？？
        if memo is None:
            memo = {}
        result = self.__class__()
        memo[id(self)] = result
        for key, value in dict.items(self):
            dict.__setitem__(result, copy.deepcopy(key, memo), copy.deepcopy(value, memo))
        return result

    def get(self, key, default=None):
        "Returns the default value if the requested data doesn't exist"
        #一层封装
        try:
            val = self[key]
        except KeyError:
            return default
        #val 为[]的情况是什么？？
        if val == []:
            return default
        return val

    def getlist(self, key):
        "Returns an empty list if the requested data doesn't exist"
        try:
            return dict.__getitem__(self, key)
        except KeyError:#multidictkeyerror
            return []

    def setlist(self, key, list_):
        dict.__setitem__(self, key, list_)

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def setlistdefault(self, key, default_list=()):
        if key not in self:
            self.setlist(key, default_list)
        return self.getlist(key)

    def appendlist(self, key, value):
        "Appends an item to the internal list associated with key"
        self.setlistdefault(key, [])
        #列表居然可以通过 + 拼接在一起
        dict.__setitem__(self, key, self.getlist(key) + [value])

    def items(self):
        """
        Returns a list of (key, value) pairs, where value is the last item in
        the list associated with the key.
        """
        return [(key, self[key]) for key in self.keys()]

    def lists(self):
        "Returns a list of (key, list) pairs."
        return dict.items(self)

    def values(self):
        "Returns a list of the last value on every key list."
        return [self[key] for key in self.keys()]

    def copy(self):
        "Returns a copy of this object."
        return self.__deepcopy__()

    def update(self, *args, **kwargs):
        "update() extends rather than replaces existing key lists. Also accepts keyword args."
        #形参只是形式上的，表示可以接受一切参数，但是实际上如果不是一个dict，那么就会直接raise error
        #上面理解出现错误，args是列表，kwargs是字典
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        if args:
            other_dict = args[0]
            if isinstance(other_dict, MultiValueDict):
                for key, value_list in other_dict.lists():
                    #下面才是正常的扩展列表的方式，通过extend
                    self.setlistdefault(key, []).extend(value_list)
            else:
                try:
                    for key, value in other_dict.items():
                        self.setlistdefault(key, []).append(value)
                except TypeError:
                    raise ValueError("MultiValueDict.update() takes either a MultiValueDict or dictionary")
        for key, value in kwargs.iteritems():
            self.setlistdefault(key, []).append(value)

class SiteNode(object):
    """Class to represent a site node (page, image or any other file)"""
    #展示site中的某个节点

    def __init__(self, url):
        self.url = url
        self.itemnames = []
        self.children = []
        self.parent = None

    def add_child(self, node):
        self.children.append(node)
        node.parent = self
 
    def to_string(self, level=0):
        #递归展示所有的节点
        #children与itemnames每一层次都会多加一定数目的空格做递进
        s = "%s%s\n" % ('  '*level, self.url)
        if self.itemnames:
            for n in self.itemnames:
                s += "%sScraped: %s\n" % ('  '*(level+1), n)
        for node in self.children:
            s += node.to_string(level+1)
        return s


class CaselessDict(dict):
    #caselessdict是不区分key大小写的字典
    #slot是什么？？
    __slots__ = ()

    def __init__(self, seq=None):
        #super方法初始化？？
        super(CaselessDict, self).__init__()
        if seq:
            self.update(seq)

    def __getitem__(self, key):
        #normalkey？？
        return dict.__getitem__(self, self.normkey(key))

    def __setitem__(self, key, value):
        dict.__setitem__(self, self.normkey(key), self.normvalue(value))

    def __delitem__(self, key):
        dict.__delitem__(self, self.normkey(key))

    def __contains__(self, key):
        return dict.__contains__(self, self.normkey(key))
    has_key = __contains__

    def __copy__(self):
        return self.__class__(self)
    copy = __copy__

    def normkey(self, key):
        """Method to normalize dictionary key access"""
        return key.lower()

    def normvalue(self, value):
        """Method to normalize values prior to be setted"""
        #封装抽象了一层，具体的情况可以再修改这个函数
        return value

    def get(self, key, def_val=None):
        return dict.get(self, self.normkey(key), self.normvalue(def_val))

    def setdefault(self, key, def_val=None):
        return dict.setdefault(self, self.normkey(key), self.normvalue(def_val))

    def update(self, seq):
        seq = seq.iteritems() if isinstance(seq, dict) else seq
        iseq = ((self.normkey(k), self.normvalue(v)) for k, v in seq)
        super(CaselessDict, self).update(iseq)
    
    #fromkeys中间的cls究竟是什么
    @classmethod
    def fromkeys(cls, keys, value=None):
        return cls((k, value) for k in keys)

    def pop(self, key, *args):
        return dict.pop(self, self.normkey(key), *args)


class MergeDict(object):
    """
    A simple class for creating new "virtual" dictionaries that actually look
    up values in more than one dictionary, passed in the constructor.

    If a key appears in more than one of the given dictionaries, only the
    first occurrence will be used.
    """
    def __init__(self, *dicts):
        self.dicts = dicts

    def __getitem__(self, key):
        for dict_ in self.dicts:
            try:
                return dict_[key]
            except KeyError:
                pass
        raise KeyError

    def __copy__(self):
        return self.__class__(*self.dicts)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def getlist(self, key):
        for dict_ in self.dicts:
            #与上面的getitem的写法区别有必要么，是因为不是一个人写的原因么
            if key in dict_.keys():
                return dict_.getlist(key)
        return []

    def items(self):
        #reduce(lambda a,b:a.extend(b), map(lambda t: t.items, self.dicts))
        item_list = []
        for dict_ in self.dicts:
            item_list.extend(dict_.items())
        return item_list

    def has_key(self, key):
        for dict_ in self.dicts:
            if key in dict_:
                return True
        return False

    __contains__ = has_key

    def copy(self):
        """Returns a copy of this object."""
        return self.__copy__()


class LocalCache(OrderedDict):
    """Dictionary with a finite number of keys.

    Older items expires first.

    """
    #orderedDict

    def __init__(self, limit=None):
        super(LocalCache, self).__init__()
        self.limit = limit

    def __setitem__(self, key, value):
        while len(self) >= self.limit:
            self.popitem(last=False)
        super(LocalCache, self).__setitem__(key, value)
