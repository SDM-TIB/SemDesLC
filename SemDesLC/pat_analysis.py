import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import re
import streamlit as st
from streamlit.components.v1 import html
import networkx as nx


def query_generation(input, endpoint):
    global newrow
    where_clause = """?patient <http://example.org/lungCancer/vocab/hasStage> ?stage. \n ?patient <http://example.org/lungCancer/vocab/hasGender> ?gender. \n ?patient <http://example.org/lungCancer/vocab/hasAgeCategory> ?ageCategory. \n OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o1. ?o1 <http://example.org/lungCancer/vocab/hasBiomarker> ?biomarker .} \n OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientRelapseProgression> ?o2. ?o2 <http://example.org/lungCancer/vocab/hasRelapse_Progression> ?relapse_or_progression .} \n OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientSmoking> ?o3. ?o3 <http://example.org/lungCancer/vocab/hasSmokingHabit> ?smokingHabit.} \n OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o4. ?o4 <http://example.org/lungCancer/vocab/treatmentType> ?treatmentType.} """
    query_select_clause = "SELECT DISTINCT ?patient ?stage ?gender ?ageCategory ?biomarker ?relapse_or_progression ?smokingHabit ?treatmentType"
    query_where_clause = """\n WHERE { \n ?patient a <http://example.org/lungCancer/vocab/Patient>."""
    patient = input['Patient_ID']
    filter_clause = f"FILTER (?patient IN (<http://example.org/lungCancer/entity/{patient}_Patient>))"
    sparql_query = query_select_clause + query_where_clause + where_clause + "\n" + filter_clause + "}"

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results["results"]["bindings"]

    out = []
    col_names = []

    for row in data:
        newrow = ''
        patient_value = row.get("patient", {}).get("value", "")
        if patient_value:
            pat_name = 'Patient'
            if pat_name not in col_names:
                col_names.append(pat_name)
            newrow = patient_value.replace("http://example.org/lungCancer/entity/", "")

        gender_value = row.get("gender", {}).get("value", "")
        if gender_value:
            gender_name = 'Gender'
            if gender_name not in col_names:
                col_names.append(gender_name)
            newrow = newrow + ", " + (gender_value.replace("http://example.org/lungCancer/entity/", ""))

        age_value = row.get("ageCategory", {}).get("value", "")
        if age_value:
            age_name = 'Age Category'
            if age_name not in col_names:
                col_names.append(age_name)
            newrow = newrow + ", " + (age_value.replace("http://example.org/lungCancer/entity/", ""))

        stage_value = row.get("stage", {}).get("value", "")
        if stage_value:
            stage_name = 'Stage'
            if stage_name not in col_names:
                col_names.append(stage_name)
            newrow = newrow + ", " + (stage_value.replace("http://example.org/lungCancer/entity/", ""))

        bio_value = row.get("biomarker", {}).get("value", "")
        if bio_value:
            bio_name = 'Biomarker'
            if bio_name not in col_names:
                col_names.append(bio_name)
            newrow = newrow + ", " + (bio_value.replace("http://example.org/lungCancer/entity/", ""))

        rel_value = row.get("relapse_or_progression", {}).get("value", "")
        if rel_value:
            rel_name = 'Relapse or Progression'
            if rel_name not in col_names:
                col_names.append(rel_name)
            newrow = newrow + ", " + (rel_value.replace("http://example.org/lungCancer/entity/", ""))

        smoking_value = row.get("smokingHabit", {}).get("value", "")
        if smoking_value:
            smoking_name = 'Smoking Habit'
            if smoking_name not in col_names:
                col_names.append(smoking_name)
            newrow = newrow + ", " + (smoking_value.replace("http://example.org/lungCancer/entity/", ""))

        treat_value = row.get("treatmentType", {}).get("value", "")
        if treat_value:
            treat_name = 'Treatment Type'
            if treat_name not in col_names:  # Check if the column name is not already present
                col_names.append(treat_name)
            newrow = newrow + ", " + (treat_value.replace("http://example.org/lungCancer/entity/", ""))

        out.append(newrow + '\n')
    col_names = list(dict.fromkeys(col_names))
    d = [x.strip().split("\n") for x in out]
    df = pd.DataFrame(d)
    data = list(df[0].apply(lambda x: x.split(",")))
    data = pd.DataFrame(data, columns=col_names)
    return data


def generate_explanation(dictionary, dict_pred_prob):
    explanation = ""
    # Explanation for prediction probabilities
    explanation += "\n\n**Prediction Probabilities:**\n\n"
    for label, probability in dict_pred_prob.items():
        explanation += f"Probability of being labeled as {label}: {float(probability) * 100:.2f}%\n"

    # Explanation for Impact of Features on Prediction
    explanation += "\n\n**Impact of Features on Prediction:**\n\n"
    for feature, weight in dictionary.items():
        feature_name = feature.replace(' ','').replace('_', ' ')
        weight_value = float(weight)
        positive_or_negative = "positive" if weight_value >= 0 else "negative"
        abs_weight_value = abs(weight_value)
        explanation += f"**{feature_name} ({weight}):** The presence of {feature_name.lower()} has a significant {positive_or_negative} impact on the prediction. "
        explanation += f"This suggests that {'patients with' if positive_or_negative == 'positive' else 'patients without'} {feature_name.lower()} are {'more' if positive_or_negative == 'positive' else 'less'} likely to be predicted as not experiencing relapse. \n\n"

    return explanation


def interpretation(file_path1, file_path2, input):
    patient = input['Patient_ID']
    # Construct the index pattern
    index_pattern = f"{patient}_Patient"
    index_pattern = re.compile(rf"^{re.escape(index_pattern)}$")
    # Initialize an empty dictionary to store feature and weights
    feature_weights_dict = {}
    pred_prob = {}
    # Define a pattern to match the numeric conditions
    pattern = r'(> |<=|<|=|\s*\d+\.\d+\s*)'

    with open(file_path1) as f:
        reader_obj = csv.DictReader(f)
        for row in reader_obj:
            # Check if the index column contains the index pattern
            if index_pattern.match(row['index']):
                feature = re.sub(pattern, '', row['features'])
                weights = row['weights']
                # Save the feature and weights into the dictionary
                feature_weights_dict[feature] = weights

    with open(file_path2) as f:
        reader_obj = csv.DictReader(f)
        for row in reader_obj:
            # Check if the index column contains the index pattern
            if index_pattern.match(row['index']):
                classes = row['class']
                prob = row['PredictionProbabilities']
                # Save the feature and weights into the dictionary
                pred_prob[classes] = prob

    exp = generate_explanation(feature_weights_dict, pred_prob)
    return exp


def lime_interpretation(dict_user):
    pat = dict_user['Patient_ID']
    if pat is not None:
        path_to_html = f'./output/Lime_{pat}-patient.html'
    else:
        st.error("Please provide valid Patient ID")

    return path_to_html


def create_network_graph(dataframe):
    # Create an empty graph
    G = nx.Graph()

    # Add edges to the graph
    for i, row in dataframe.iterrows():
        G.add_edge(row['source'], row['target'])

    # Convert the networkx graph to a Cytoscape compatible format
    elements = nx.cytoscape_data(G)['elements']

    return elements


def generate_dot_style(data):
    dot_style = ''
    dot_style += ' [dir=forward] [arrowhead=normal]'
    return dot_style



def gen_graph(df):
    patient_id = df['Patient'].iloc[0]
    edges = []
    # Iterate through each row in the dataframe
    for _, row in df.iterrows():
        # Iterate through each column (excluding 'Patient')
        for col, val in row.items():
            if col == 'Patient':
                continue
            # If the value is a list, create an edge for each element in the list
            if isinstance(val, list):
                for v in val:
                    edges.append((patient_id, col, v))
            else:
                # If it's not a list, create a single edge
                edges.append((patient_id, col, val))

    # Create a DataFrame from the list of edges
    edges_df = pd.DataFrame(edges, columns=['source', 'value', 'target'])

    edges_df['source'] = edges_df['source'].str.replace("_Patient", "")

    # Generate network graph
    st.subheader('Patient Characteristics 🤒')
    elements = create_network_graph(edges_df)

    # Convert elements to Graphviz DOT format
    dot = 'graph {'
    for edge in elements['edges']:
        dot_style = generate_dot_style(edge['data'])
        source_color = 'orange'
        target_color = 'lightblue1'
        dot += f"\n    {edge['data']['source']} [style=filled, fillcolor={source_color}];"
        dot += f"\n    {edge['data']['target']} [style=filled, fillcolor={target_color}];"
        dot += f"\n    {edge['data']['source']} -- {edge['data']['target']}{dot_style}"

    dot += '\n}'

    # Display network graph using st.graphviz_chart
    st.graphviz_chart(dot, use_container_width=True)


def main(my_dict):
    dataframe = query_generation(my_dict, "https://kg_lc:8890/sparql")
    exp = interpretation('./app/files/lime_interpretation_features.csv',
                         './app/files/predicition_probabilities.csv', my_dict)
    return dataframe, exp


border = 'rgb(250,250,250,.2)'  # dark mode


def ChangeButtonColour(widget_label, font_color, hover_color, background_color='transparent', width=None):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}';
                    elements[i].style.width = '{width}px';
                    elements[i].onmouseover = function() {{ 
                        this.style.color = '{hover_color}';
                        this.style.borderColor = '{hover_color}';
                    }};
                    elements[i].onmouseout = function() {{ 
                        this.style.color = '{font_color}';
                        this.style.borderColor = '{border}';
                    }};
                    elements[i].onfocus = function() {{
                        this.style.boxShadow = '{hover_color} 0px 0px 0px 0.2rem';
                        this.style.borderColor = '{hover_color}';
                        this.style.color = '{hover_color}';
                    }};
                    elements[i].onblur = function() {{
                        this.style.boxShadow = 'none';
                        this.style.borderColor = '{border}';
                        this.style.color = '{font_color}';
                    }};
                }}
            }}
        </script>
        """
    return st.components.v1.html(f"{htmlstr}", height=0, width=0)


def generate_patient():
    #st.title("Patient-Centric Analysis 👨‍⚕️👩‍⚕️")
    button_width = 176
    col1, col2 = st.columns([0.1, 0.5])
    # Collect user inputs
    with col1:
        patient = st.text_input("Enter Patient ID")
    # Create a dictionary
    dict_user = {
        "Patient_ID": patient
    }

    # Initialize the key in session state
    if 'clicked' not in st.session_state:
        st.session_state.clicked = {'Show Analysis': False, 'LIME Interpretation': False}

    # Function to update the value in session state
    def clicked(button):
        st.session_state.clicked[button] = True

    button1 = st.button("Show Analysis")
    ChangeButtonColour('Show Analysis', 'white', 'black', '#1b4965', width=button_width)

    if button1:
        clicked('Show Analysis')

    if st.session_state.clicked.get('Show Analysis'):
        st.session_state.result, st.session_state.exp = main(dict_user)
        gen_graph(st.session_state.result)
        st.dataframe(st.session_state.result)

    button2 = st.button("LIME Interpretation")
    ChangeButtonColour('LIME Interpretation', 'white', 'black', '#1b4965', width=button_width)

    if button2:
        clicked('LIME Interpretation')

    if st.session_state.clicked.get('LIME Interpretation'):
        path = lime_interpretation(dict_user)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
            st.components.v1.html(html, height=300, width=1000)
        st.session_state.result, st.session_state.exp = main(dict_user)
        button3 = st.button("SemDesLC Explanation")
        ChangeButtonColour('SemDesLC Explanation', 'white', 'black', '#1b4965', width=button_width)

        if button3:
            with st.chat_message("assistant"):
                st.write("I am here to help you understand the above interpretation")
                st.write(st.session_state.exp)


if __name__ == '__main__':
    generate_patient()
