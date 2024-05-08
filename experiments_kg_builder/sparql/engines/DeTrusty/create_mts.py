from DeTrusty.Molecule.MTCreation import create_rdfmts

endpoints = {
    "http://kg_lc:8890/sparql": {},
    "http://kg_semdeslc:8890/sparql": {}
}
create_rdfmts(endpoints, 'rdfmts_virtuoso.json', False)

endpoints = {
    "http://kg_lc_fuseki:3030/lc/query": {},
    "http://kg_semdeslc_fuseki:3030/interpretme/query": {}
}
create_rdfmts(endpoints, 'rdfmts_fuseki.json', False)
