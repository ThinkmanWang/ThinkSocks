# -*- coding: utf-8 -*-

import uuid
import time
import math
import redis

def acquire_lock(conn=None, lockname='', acquire_timeout=20):
    '''使用redis实现最简单的锁
    使用setnx命令设置锁的值， 设置成功即为获取锁成功
    '''
    return acquire_lock_with_timeout(conn, lockname, acquire_timeout)

def release_lock(conn=None, lockname='', identifier=''):
    pipe = conn.pipeline(True)
    lockname = "lock:" + lockname
    while 1:
        try:
            pipe.watch(lockname)
            if conn.get(lockname) == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass
    return False

def acquire_lock_with_timeout(conn=None, lockname='', acquire_timeout=10, lock_timeout=60):
    '''带有超时限制特性的锁'''
    identifier = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    lock_timeout = int(math.ceil(lock_timeout))
    end_time = time.time() + acquire_timeout
    while time.time() < end_time:
        if conn.setnx(lockname, identifier):
            conn.expire(lockname, lock_timeout)
            return identifier
        elif not conn.ttl(lockname):
            conn.expire(lockname, lock_timeout)
        time.sleep(.001)
    return None

# if __name__ == '__main__':
#     r = redis.StrictRedis(connection_pool=g_redis_pool)
#     szID = acquire_lock_with_timeout(r, "migu_register_fxxk", acquire_timeout=10, lock_timeout=60)
#     if False == is_empty_string(szID):
#         print szID
#     else:
#         print "FXXK"