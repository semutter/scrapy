"""Helper functions for working with templates"""

import os
import re
import string

def render_templatefile(path, **kwargs):
    with open(path, 'rb') as file:
        raw = file.read()
    #string居然还有template？？
    content = string.Template(raw).substitute(**kwargs)
    #rstrip函数，把右边的.tmpl删除
    with open(path.rstrip('.tmpl'), 'wb') as file:
        file.write(content)
    #渲染完成后删除该tmpl模版文件
    if path.endswith('.tmpl'):
        os.remove(path)

CAMELCASE_INVALID_CHARS = re.compile('[^a-zA-Z\d]')
def string_camelcase(string):
    """ Convert a word  to its CamelCase version and remove invalid chars

    >>> string_camelcase('lost-pound')
    'LostPound'

    >>> string_camelcase('missing_images')
    'MissingImages'

    """
    #camelcase 是通过string.title()方法实现的
    #re.sub(r'[^a-zA-Z\d]', '', string.title())
    return CAMELCASE_INVALID_CHARS.sub('', string.title())
