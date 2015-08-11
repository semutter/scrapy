import sys
import os
from ConfigParser import SafeConfigParser
from operator import itemgetter

def build_component_list(base, custom):
    """Compose a component list based on a custom and base dict of components
    (typically middlewares or extensions), unless custom is already a list, in
    which case it's returned.
    """
    #对custion判断是否为list或者tuple，如果是，直接返回，如果不是，对base更新custom中的内容，并返回更新完的value部位空的那些key
    #并按value排序
    if isinstance(custom, (list, tuple)):
        return custom
    compdict = base.copy()
    compdict.update(custom)
    return [k for k, v in sorted(compdict.items(), key=itemgetter(1)) \
        if v is not None]

def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    #dict函数可以将一个mapping直接转化为字典
    return dict(x.split('=', 1) for x in arglist)

def closest_scrapy_cfg(path='.', prevpath=None):
    """Return the path to the closest scrapy.cfg file by traversing the current
    directory and its parents
    """
    #递归查找并返回配置文件
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'scrapy.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_scrapy_cfg(os.path.dirname(path), path)

def init_env(project='default', set_syspath=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Scrapy settings module and modifies the Python path to
    be able to locate the project module.
    """
    """Get Scrapy config file as a SafeConfigParser"""
    #利用safeconfigparse()去解析已经有的配置文件列表
    sources = get_sources(use_closest)
    cfg = SafeConfigParser()
    cfg.read(sources)#读取文件列表
    return cfg

def get_sources(use_closest=True):
    #返回可能的scrapy配置文件的abspath列表
    sources = ['/etc/scrapy.cfg', r'c:\scrapy\scrapy.cfg', \
        os.path.expanduser('~/.scrapy.cfg')]
    if use_closest:
        sources.append(closest_scrapy_cfg())
    return sources
