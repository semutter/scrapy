"""Helper functions for scrapy.http objects (Request, Response)"""

#weakref是什么鬼？？
#A primary use for weak references is to implement caches or mappings holding large objects,
#where it’s desired that a large object not be kept alive solely because it appears in a cache or mapping. 
#弱引用，当一个对象只剩弱引用时，可能会被GC回收，回收时调用创建时声明的callback函数进行相关操作
#wekref可以做缓存用

import weakref

#urlparse作用是
#它从urlstring中取得URL，并返回元组 (scheme, netloc, path, parameters, query, fragment)
#<scheme>://<netloc>/<path>;<params>?<query>#<fragment>
#Return a 6-tuple: (scheme, netloc, path, params, query, fragment). 
from urlparse import urlparse

_urlparse_cache = weakref.WeakKeyDictionary()
def urlparse_cached(request_or_response):
    """Return urlparse.urlparse caching the result, where the argument can be a
    Request or Response object
    """
    if request_or_response not in _urlparse_cache:
        _urlparse_cache[request_or_response] = urlparse(request_or_response.url)
    return _urlparse_cache[request_or_response]
