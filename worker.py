from rqalpha import run_file,run_code

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-06-10",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }

  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": False
    }
  }
}




#strategy_file_path = "../examples/buy_and_hold.py"

#run_file(strategy_file_path, config)
#exit(0)
from redis_queue import StrategyQueue,ResultQueue
import json
import codecs
#with codecs.open("../examples/buy_and_hold.py", encoding="utf-8") as f:
#    source_code = f.read()
while True:
    result =  StrategyQueue.get_wait()
    if not result:
       # result=run_code(code=source_code, config=config)
        break
    result=json.loads(result)
    if 'config' in result and 'plot' in result['config']:
        result['config']['plot']=False
    print("\n\nrecieve a strategy ")
    raw_result=run_code(code=result['source_code'], config=result['config'])
    try:
        x_list=raw_result['sys_analyser']['portfolio'].index.strftime('%Y-%m-%d').tolist()
    except Exception:
        continue
    portfolio_list = raw_result['sys_analyser']['portfolio'].loc[:,'market_value'].tolist()
    benchmark_list=raw_result['sys_analyser']['benchmark_portfolio'].loc[:,'market_value'].tolist()
    last_day=raw_result['sys_analyser']['stock_positions'].index[-1]
    stock_positions = raw_result['sys_analyser']['stock_positions'].loc[last_day,'order_book_id']
    if isinstance (stock_positions,str):
        stock_positions_list=[stock_positions,]
    else:
        stock_positions_list=stock_positions.tolist()
    result['result']={"summary":raw_result['sys_analyser']['summary'],"date":x_list,"portfolio":portfolio_list,"benchmark_portfolio":benchmark_list,"positions":stock_positions_list}
    del result['source_code']
    StrategyQueue.get_db().set(result['config'].get('strategy_id','default_strategy_id'),json.dumps(result),ex=300)
    pass


