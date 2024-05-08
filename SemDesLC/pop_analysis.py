import pandas as pd
from scipy import stats
from DeTrusty import run_query
from DeTrusty.Molecule.MTManager import Config
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html
from SPARQLWrapper import SPARQLWrapper, JSON

def federated(query):
    query_result = run_query(query, config=Config(), join_stars_locally=False)
    columns = query_result['head']['vars']
    df_result = pd.DataFrame(columns=columns)
    cardinality = 0
    for res in query_result['results']['bindings']:
        df_result.loc[cardinality] = [res[var]['value'] for var in columns]
        cardinality += 1

    return df_result


def vis(result, patient_num, feature_num):
    result['feature'] = result['feature'].str.replace(r'%.*', '', regex=True)
    feature_num['feature'] = feature_num['feature'].str.replace(r'%.*', '', regex=True)
    result['value'] = pd.to_numeric(result['value'], errors='coerce')
    print(result)
    print(feature_num)
    # Set style
    sns.set(style="whitegrid")
    # Plot KDE plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(result['value'], color='skyblue', fill=True)
    # Calculate p-value for overall distribution
    overall_p_value = stats.ttest_1samp(result['value'], 0)[1]
    # Add overall p-value as title
    plt.title(f'Kernel Density Estimation Plot (Overall p-value = {overall_p_value:.3f})', loc='center', fontsize=16,pad=20)
    plt.xlabel('Value', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("pop_analysis.png")

    # Create an interactive bar plot with Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=result['value'], y=result['feature'], orientation='h',
                         marker_color='blue',
                         hoverinfo='x+text',  # Display x-axis value and custom hover text
                         hovertext=[f"Number of patients: {feature_num[feature_num['feature'] == feature]['num'].iloc[0]}" for feature in
                                    result['feature']]))

    fig.update_layout(title='Total number of patients in the sub-population: ' + str(patient_num),
                      xaxis_title='Value',
                      yaxis_title='Feature',
                      template='seaborn')
    fig.write_html("feature_weights.html")


def query_generation(input_data, endpoint1, endpoint2):
    where_clause_endpoint1 = {
        "PDL1":"""OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o1. ?o1 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/PDL1>.}""",
        "ALK": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o2. ?o2 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/ALK>.}""",
        "EGFR": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o3. ?o3 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/EGFR>.}""",
        "ROS1": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o4. ?o4 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/ROS1>.}""",
        "BRAF": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o5. ?o5 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/BRAF>.}""",
        "RET": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o6. ?o6 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/RET>.}""",
        "KRAS": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o7. ?o7 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/KRAS>.}""",
        "MET": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o8. ?o8 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/MET>.}""",
        "HER2": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientBiomarker> ?o9. ?o9 <http://example.org/lungCancer/vocab/hasBiomarker> <http://example.org/lungCancer/entity/HER2>.}""",
        "IIIA":"""?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IIIA>.""",
        "IIIB":"""?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IIIB>.""",
        "IVB":"""?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IVB>.""",
        "IVA": """?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IVB>.""",
        "IV":"""?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IV>.""",
        "IA":"""?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IA>.""",
        "IIIC": """?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IIIC>.""",
        "IB": """?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IB>.""",
        "IA1": """?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IA1>.""",
        "IA2": """?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IA2>.""",
        "IIA": """?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IIA>.""",
        "IIB": """?patient <http://example.org/lungCancer/vocab/hasStage> <http://example.org/lungCancer/entity/IIB>.""",
        "Female":"""?patient <http://example.org/lungCancer/vocab/hasGender> <http://example.org/lungCancer/entity/Female>.""",
        "Male": """?patient <http://example.org/lungCancer/vocab/hasGender> <http://example.org/lungCancer/entity/Male>.""",
        "Young": """?patient <http://example.org/lungCancer/vocab/hasAgeCategory> <http://example.org/lungCancer/entity/Young>.""",
        "Old": """?patient <http://example.org/lungCancer/vocab/hasAgeCategory> <http://example.org/lungCancer/entity/Old>.""",
        "Relapse": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientRelapseProgression> ?o11. ?o11 <http://example.org/lungCancer/vocab/hasRelapse_Progression> <http://example.org/lungCancer/entity/Relapse>.}""",
        "Progression": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientRelapseProgression> ?o12. ?o12 <http://example.org/lungCancer/vocab/hasRelapse_Progression> <http://example.org/lungCancer/entity/Progression>.}""",
        "No_Progression": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientRelapseProgression> ?o13. ?o13 <http://example.org/lungCancer/vocab/hasRelapse_Progression> <http://example.org/lungCancer/entity/No_Progression>.}""",
        "CurrentSmoker": """?patient <http://example.org/lungCancer/vocab/patientSmoking> ?o14. ?o14 <http://example.org/lungCancer/vocab/hasSmokingHabit> <http://example.org/lungCancer/entity/CurrentSmoker>.""",
        "NonSmoker": """?patient <http://example.org/lungCancer/vocab/patientSmoking> ?o15. ?o15 <http://example.org/lungCancer/vocab/hasSmokingHabit> <http://example.org/lungCancer/entity/NonSmoker>.""",
        "FormerSmoker": """?patient <http://example.org/lungCancer/vocab/patientSmoking> ?o16. ?o16 <http://example.org/lungCancer/vocab/hasSmokingHabit> <http://example.org/lungCancer/entity/FormerSmoker>.""",
        "Chemotherapy_Adjuvant": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o17. ?o17 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Chemotherapy_Adjuvant>.}""",
        "Open_Surgical_Procedure": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o18. ?o18 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Open_Surgical_Procedure>.}""",
        "Intravenous_Chemotherapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o19. ?o19 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Intravenous_Chemotherapy>.}""",
        "Whole_Brain_Radiation_Therapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o20. ?o20 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Whole_Brain_Radiation_Therapy>.}""",
        "Radiotherapy_To_Lung": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o21. ?o21 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Radiotherapy_To_Lung>.}""",
        "Immunotherapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o22. ?o22 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Immunotherapy>.}""",
        "Molecular_Targeted_Therapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o23. ?o23 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Molecular_Targeted_Therapy>.}""",
        "Thoracoscopy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o24. ?o24 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Thoracoscopy>.}""",
        "Radiotherapy_To_Bone": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o25. ?o25 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Radiotherapy_To_Bone>.}""",
        "Neoadjuvant_Chemotherapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o26. ?o26 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Neoadjuvant_Chemotherapy>.}""",
        "Oral_Chemotherapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o27. ?o27 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Oral_Chemotherapy>.}""",
        "Concurrent_Chemoradiotherapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o28. ?o28 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Concurrent_Chemoradiotherapy>.}""",
        "Sequential_Chemoradiation": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o29. ?o29 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Sequential_Chemoradiation>.}""",
        "Chemoradiotherapy_Adjuvant": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o30. ?o30 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Chemoradiotherapy_Adjuvant>.}""",
        "Neoadjuvant_Chemoradiotherapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o31. ?o31 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Neoadjuvant_Chemoradiotherapy>.}""",
        "Hormone_Therapy": """OPTIONAL{?patient <http://example.org/lungCancer/vocab/patientTreatmentType> ?o32. ?o32 <http://example.org/lungCancer/vocab/treatmentType> <http://example.org/lungCancer/entity/Hormone_Therapy>.}""",

    }

    where_clause_endpoint2 = """?entity a <http://semdeslc.org/vocab/TargetEntity> .
           ?entity <http://semdeslc.org/vocab/hasInterpretedFeature> ?interpretedFeature .
    ?entity <http://www.w3.org/2002/07/owl#sameAs> ?patient .
    ?interpretedFeature  <http://semdeslc.org/vocab/hasFeatureWeight> ?featureWeight .
    ?featureWeight <http://semdeslc.org/vocab/hasFeature> ?feature .
    ?featureWeight <http://semdeslc.org/vocab/hasWeight> ?value .
    ?entity <http://semdeslc.org/vocab/hasEntityClassProbability> ?classProb .
    ?classProb <http://semdeslc.org/vocab/hasPredictionProbability> ?probability .
    ?classProb <http://semdeslc.org/vocab/hasClass> ?targetClass ."""

    query_select_clause = "SELECT DISTINCT ?feature ?value"
    query_where_clause = """ ?patient a <http://example.org/lungCancer/vocab/Patient>. \n"""

    if "Female" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Female"] + " \n"
    if "Male" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Male"] + " \n"
    if "Young" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Young"] + " \n"
    if "Old" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Old"] + " \n"
    if "CurrentSmoker" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["CurrentSmoker"] + " \n"
    if "NomSmoker" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["NomSmoker"] + " \n"
    if "FormerSmoker" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["FormerSmoker"] + " \n"
    if "IA" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IA"] + " \n"
    if "IA1" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IA1"] + " \n"
    if "IA2" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IA2"] + " \n"
    if "IB" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IB"] + " \n"
    if "IIA" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IIA"] + " \n"
    if "IIB" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IIB"] + " \n"
    if "IIIA" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IIIA"] + " \n"
    if "IIIB" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IIIB"] + " \n"
    if "IIIC" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IIIC"] + " \n"
    if "IIIB" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IIIB"] + " \n"
    if "IV" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IV"] + " \n"
    if "IVA" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IVA"] + " \n"
    if "IVB" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["IVB"] + " \n"
    if "ALK" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["ALK"] + " \n"
    if "EGFR" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["EGFR"] + " \n"
    if "ROS1" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["ROS1"] + " \n"
    if "PDL1" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["PDL1"] + " \n"
    if "BRAF" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["BRAF"] + " \n"
    if "RET" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["RET"] + " \n"
    if "MET" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["MET"] + " \n"
    if "KRAS" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["KRAS"] + " \n"
    if "HER2" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["HER2"] + " \n"
    if "Relapse" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Relapse"] + " \n"
    if "Progression" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Progression"] + " \n"
    if "No_Progression" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["No_Progression"] + " \n"
    if "Intravenous_Chemotherapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Intravenous_Chemotherapy"] + " \n"
    if "Immunotherapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Immunotherapy"] + " \n"
    if "Radiotherapy_To_Bone" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Radiotherapy_To_Bone"] + " \n"
    if "Whole_Brain_Radiation_Therapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Whole_Brain_Radiation_Therapy"] + " \n"
    if "Molecular_Targeted_Therapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Molecular_Targeted_Therapy"] + " \n"
    if "Oral_Chemotherapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Oral_Chemotherapy"] + " \n"
    if "Thoracoscopy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Thoracoscopy"] + " \n"
    if "Neoadjuvant_Chemotherapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Neoadjuvant_Chemotherapy"] + " \n"
    if "Open_Surgical_Procedure" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Open_Surgical_Procedure"] + " \n"
    if "Chemotherapy_Adjuvant" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Chemotherapy_Adjuvant"] + " \n"
    if "Concurrent_Chemoradiotherapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Concurrent_Chemoradiotherapy"] + " \n"
    if "Radiotherapy_To_Lung" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Radiotherapy_To_Lung"] + " \n"
    if "Sequential_Chemoradiation" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Sequential_Chemoradiation"] + " \n"
    if "Chemoradiotherapy_Adjuvant" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Chemoradiotherapy_Adjuvant"] + " \n"
    if "Neoadjuvant_Chemoradiotherapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Neoadjuvant_Chemoradiotherapy"] + " \n"
    if "Hormone_Therapy" in input_data:
        query_where_clause = query_where_clause + where_clause_endpoint1["Hormone_Therapy"] + " \n"


    service1 = "SERVICE <" + endpoint2 + "> "
    service2 = "SERVICE <" + endpoint1 + "> "
    query_where_clause1 = "WHERE { \n"+ service1 + "{\n" + where_clause_endpoint2 + "}"
    query_where_clause2 = "\n"+ service2 + "{\n" + query_where_clause  + "}"
    sparqlQuery = query_select_clause + " " + query_where_clause1 + "" + query_where_clause2 + "}"
    print(sparqlQuery)

    res = federated(sparqlQuery)
    res['feature'] = res['feature'].str.replace('http://semdeslc.org/entity/', '')
    # res.to_csv("pop_analysis.csv", index=False)

    sparqlQuery_numP = "SELECT COUNT(DISTINCT ?patient) AS ?numP" + " WHERE { " + query_where_clause +" }"
    print(sparqlQuery_numP)
    sparql = SPARQLWrapper(endpoint1)
    sparql.setQuery(sparqlQuery_numP)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = results["results"]["bindings"]
    patient_num = data[0]['numP']['value']
    print(patient_num)

    query_select_clause_numF = "SELECT DISTINCT ?feature (COUNT(?patient) AS ?num)"
    grp = "GROUP BY ?feature"
    sparqlQuery_numF = query_select_clause_numF + " " + query_where_clause1 + "" + query_where_clause2 + "}" + grp
    print(sparqlQuery_numF)
    feature_num = federated(sparqlQuery_numF)
    feature_num['feature'] = feature_num['feature'].str.replace('http://semdeslc.org/entity/', '')
    vis(res, patient_num, feature_num)

    return res, patient_num, feature_num

def main(my_dict):
    flattened_values = [item for sublist in my_dict.values() for item in
                        (sublist if isinstance(sublist, list) else [sublist])]
    res, num, feature_num = query_generation(flattened_values, "http://kg_lc:8890/sparql", "http://kg_semdeslc:8890/sparql")
    return res, num, feature_num


border = 'rgb(250,250,250,.2)' #dark mode

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

def generate_population():
    button_width = 155
    # Collect user inputs
    gender = st.selectbox("Gender", ["","Female", "Male"])
    age = st.selectbox("Age Category", ["","Young", "Old"])
    smoker = st.selectbox("Smoking Habit", ["","CurrentSmoker", "FormerSmoker","NonSmoker"])
    stage = st.selectbox("Stages", ["","IA","IA1","IA2","IB","IIA","IIB","IIIA","IIIB","IIIC","IV","IVA","IVB"])
    biomarker = st.multiselect("Mutation", ["","EGFR", "ALK", "PDL1","ROS1","BRAF","RET","KRAS","MET","HER2"])
    relapse = st.selectbox("Relapse Progression",["","Progression", "No_Progression", "Relapse"])
    TreatmentType = st.multiselect("Treatment Type",["","Radiotherapy_To_Bone", "Intravenous_Chemotherapy", "Immunotherapy", "Whole_Brain_Radiation_Therapy",
                     "Molecular_Targeted_Therapy", "Oral_Chemotherapy", "Thoracoscopy", "Neoadjuvant_Chemotherapy",
                     "Open_Surgical_Procedure", "Chemotherapy_Adjuvant", "Concurrent_Chemoradiotherapy", "Radiotherapy_To_Lung",
                     "Sequential_Chemoradiation", "Chemoradiotherapy_Adjuvant", "Neoadjuvant_Chemoradiotherapy",
                     "Hormone_Therapy"])
    # Create a dictionary
    dict_user = {
        "Gender": gender,
        "Age_Category": age,
        "Smoking_Habits": smoker,
        "Cancer_Stage": stage,
        "Mutation": biomarker,
        "Relapse": relapse,
        "TreatmentType": TreatmentType
    }

    # Initialize the key in session state
    if 'clicked' not in st.session_state:
        st.session_state.clicked = {'Execute': False, 'Visualize': False}

    # Function to update the value in session state
    def clicked(button):
        st.session_state.clicked[button] = True

    button1 = st.button('Execute')
    ChangeButtonColour('Execute', 'white', 'black', '#1b4965', width=button_width)

    if button1:
        clicked('Execute')

    button2 = st.button('Visualize')
    ChangeButtonColour('Visualize', 'white', 'black', '#1b4965', width=button_width)

    if button2:
        clicked('Visualize')

    if st.session_state.clicked.get('Execute', False):
        st.session_state.result, st.session_state.patient_num, st.session_state.feature_num = main(dict_user)
        st.dataframe(st.session_state.result)

    if st.session_state.clicked.get('Visualize', False):
        vis(st.session_state.result, st.session_state.patient_num, st.session_state.feature_num)
        with open("./feature_weights.html", 'r', encoding='utf-8') as f:
            html = f.read()
            st.components.v1.html(html, width=1000, height=500)

        st.image('./pop_analysis.png', width=800)



if __name__ == '__main__':
    generate_population()
