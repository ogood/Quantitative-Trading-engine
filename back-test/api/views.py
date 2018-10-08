from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json,redis

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
            pool = redis.ConnectionPool(host='203.195.196.119', password='345#$%678^&*', port=6333, db=2)  # 实现一个连接池
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
StrategyQueue.get_db()
@api_view(['GET', 'POST'])
def index(request):
    """
    post a strategy or get the backtest result .
    """
    if request.method == 'GET':
        strategy_id = request.query_params.get('strategy_id', None)
        if strategy_id:

            db=StrategyQueue.get_db()
            bt_result=db.get(strategy_id)
            if bt_result is not None:
                return Response(json.loads(bt_result))
            else:
                return Response({"status":'strategy not found'})

        return Response({"status":'invalid parameter'})

    elif request.method == 'POST':
        if 'config' in request.data and 'source_code' in request.data:
            db = StrategyQueue.get_db()
            StrategyQueue.put(json.dumps(request.data))
            return Response(status=status.HTTP_201_CREATED)
        return Response({"status": 'invalid data'})


       
# Create your views here.
