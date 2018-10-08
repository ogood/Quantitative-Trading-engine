import redis

class RedisQueue(object):
    _con=None
    _db=None
    def __init__(self, name,  **redis_kwargs):
       # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
       self.get_db()
       self.key = '%s' %( name)
    @classmethod
    def get_db(cls):
        if cls._db==None:
            pool = redis.ConnectionPool(host='***', password='***', port=***, db=2)  # 实现一个连接池
            cls._db = redis.Redis(connection_pool=pool)
        return cls._db
    def qsize(self):
        return self.get_db().llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.get_db().rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.get_db().blpop(self.key, timeout=timeout)
        if item:
            item = item[1]  # 返回值为一个tuple
            return item.decode('utf-8')
        else:
            return None

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.get_db().lpop(self.key)
        return item


StrategyQueue = RedisQueue('strategy_will_backtest')
ResultQueue = RedisQueue('strategy_backtest_result')