from time import time
from TravSHACL import parse_heuristics, GraphTraversal, ShapeSchema

start = time()
heuristics = parse_heuristics('TARGET IN BIG')

shape_schema = ShapeSchema(
    schema_dir='/shapes/',
    endpoint='http://kg_lc:8890/sparql/',
    graph_traversal=GraphTraversal.DFS,
    heuristics=heuristics,
    use_selective_queries=True
)

shape_schema.validate()
end = time()
print(int((end - start) * 1000))
