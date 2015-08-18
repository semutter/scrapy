"""
Scheduler queues
"""
#管理器队列（待处理）
import marshal, cPickle as pickle

from queuelib import queue

def _serializable_queue(queue_class, serialize, deserialize):

    class SerializableQueue(queue_class):

        def push(self, obj):
            s = serialize(obj)
            super(SerializableQueue, self).push(s)

        def pop(self):
            s = super(SerializableQueue, self).pop()
            if s:
                return deserialize(s)

    return SerializableQueue

def _pickle_serialize(obj):
    try:
        #pickle.dumps的参数protocol协议为0：ascii，为1：二进制，为2，python2.3新支持的
        return pickle.dumps(obj, protocol=2)
    except pickle.PicklingError as e:
        raise ValueError(str(e))

#构造序列化的队列类
PickleFifoDiskQueue = _serializable_queue(queue.FifoDiskQueue, \
    _pickle_serialize, pickle.loads)
PickleLifoDiskQueue = _serializable_queue(queue.LifoDiskQueue, \
    _pickle_serialize, pickle.loads)
MarshalFifoDiskQueue = _serializable_queue(queue.FifoDiskQueue, \
    marshal.dumps, marshal.loads)
MarshalLifoDiskQueue = _serializable_queue(queue.LifoDiskQueue, \
    marshal.dumps, marshal.loads)
FifoMemoryQueue = queue.FifoMemoryQueue
LifoMemoryQueue = queue.LifoMemoryQueue
