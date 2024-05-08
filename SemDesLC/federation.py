import streamlit as st
from InterpretME.federated_query_engine import configuration, federated

def federation_query():
    # Enter SPARQL endpoints for Federated Query Processing
    endpoint1 = st.text_input("SemDesLC Endpoint")
    endpoint2 = st.text_input("Input Endpoint")

    # Add an input text area for the SPARQL query
    input_query = st.text_area("Enter your SPARQL query here", height=200)

    # Create a button to trigger query execution
    if st.button("Execute Query"):
        if input_query:
            # Execute the query on the first endpoint
            config = configuration(interpretme_endpoint=endpoint1, input_endpoint=endpoint2)
            query_answer = federated(input_query, config)
            st.write("Results from Query")
            st.write(query_answer)

            # Feature selection
            selected_feature = st.selectbox("Select Feature:", query_answer['feature'].unique())

            # Filter DataFrame based on selected feature
            filtered_df = query_answer[query_answer['feature'] == selected_feature]

            # Display filtered DataFrame
            st.write(filtered_df)
        else:
            st.error("Please enter a SPARQL query.")