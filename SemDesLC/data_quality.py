import streamlit as st
import os
from TravSHACL import parse_heuristics, GraphTraversal, ShapeSchema
from rdflib import Graph
from streamlit_agraph import agraph, Node, Edge, Config

SCHEMA_PATH = os.environ.get('SCHEMA_PATH', '')
ENDPOINT = os.environ.get('ENDPOINT', '')
prio_target = 'TARGET'
prio_degree = 'IN'
prio_number = 'BIG'

def travshacl():
    st.title("Validating Data Quality :hammer_and_wrench:")
    schema_path = st.text_input('Enter SHACL Shape Schema Path', value=SCHEMA_PATH)
    endpoint = st.text_input('Enter the SPARQL Endpoint', value=ENDPOINT)
    path_results = st.text_input("Path to store validation results:")
    if st.button("Run Validation"):
        validate(schema_path, endpoint, path_results)

def validate(schema_path, endpoint, path_results):
    st.write(f"Validating over provided schema path: {schema_path} and endpoint: {endpoint}")
    shape_schema = ShapeSchema(
        schema_dir=schema_path,
        endpoint=endpoint,
        graph_traversal=GraphTraversal.DFS,
        heuristics=parse_heuristics(prio_target + ' ' + prio_degree + ' ' + prio_number),
        use_selective_queries=True,
        max_split_size=256,
        output_dir=path_results,
        order_by_in_queries=False,
        save_outputs=True
    )
    result = shape_schema.validate()
    st.write("Validation Result:", result)

if __name__ == "__main__":
    travshacl()