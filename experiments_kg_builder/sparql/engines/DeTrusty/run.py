from DeTrusty import get_config, run_query
import sys

query = '/queries/' + sys.argv[1] + '.sparql'
config = get_config(sys.argv[2])
result = run_query(query, config=config, join_stars_locally=False)
print(sys.argv[1] + ',' + str(result['execution_time']) + ',' + str(result['cardinality']))
