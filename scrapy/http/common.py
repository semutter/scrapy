#一个函数使得无法直接赋值，告诉使用者，新的方法为.replace()
def obsolete_setter(setter, attrname):
    def newsetter(self, value):
        c = self.__class__.__name__
        msg = "%s.%s is not modifiable, use %s.replace() instead" % (c, attrname, c)
        raise AttributeError(msg)
    return newsetter
