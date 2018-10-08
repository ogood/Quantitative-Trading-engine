from redis_queue import StrategyQueue,ResultQueue
import codecs,json
config = {
    "strategy_id":"225",
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-06-10",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }

  },
  "extra": {
    "log_level": "error"
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": False
    }
  }
}
with codecs.open("../examples/buy_and_hold.py", encoding="utf-8") as f:
    source_code = f.read()
    data={
        "source_code":source_code,#json.dumps(data1)
        "config":config
    }
    data=json.dumps(data)
    StrategyQueue.put(data)
    print(StrategyQueue.qsize())
    result =  ResultQueue.get_db().get(config['strategy_id'])
    if result is not None:
       print( json.loads(result))
    pass

