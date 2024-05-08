import streamlit as st
import base64
import json
import plotly.graph_objects as go
from predictive_pipeline import main_process
from documentation import doc
from data_quality import travshacl
from federation import federation_query
from visualization import visualization
from pat_analysis import generate_patient
from pop_analysis import generate_population
from rules import generate_rules
from streamlit.components.v1 import html
from streamlit_lottie import st_lottie
from streamlit_extras.badges import badge

st.set_page_config(layout="wide")

VALID_USERNAME = 'user123'
VALID_PASSWORD = 'roger'
def main_updated():

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        app_content()

def load_lottie_file(filepath:str):
    with open(filepath, 'r') as f:
        return json.load(f)

include_animation = load_lottie_file('images/animation.json')

def login_page():
    st.title("Welcome to SemDesLC!")
    x, y = st.columns([0.3,0.63])
    with x:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
            else:
                st.error("Invalid username or password")
    with y:
        st_lottie(
            include_animation,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=None,
            width=None,
            key=None,
        )
def authenticate(username, password):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return True
    else:
        return False


border = 'rgb(250,250,250,.2)' # for dark mode
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


def display_train():
    train_content = st.sidebar.selectbox("Train Layer:", ["None","Data Quality", "Predictive Pipeline"])
    if train_content == "Data Quality":
        travshacl()
    elif train_content == "Predictive Pipeline":
        main_process()

def display_deduce():
    deduce_content = st.sidebar.selectbox("Deduce Layer", ["None","Visualization", "SemDesLC KG"])
    if deduce_content == "Visualization":
        visualization()
    elif deduce_content == "SemDesLC KG":
        federation_query()

def display_explain():
    explain_content = st.sidebar.selectbox("Explain Layer",
                                       ["None","Symbolic Learning", "Patient-centric Analysis", "Population-centric Analysis"])
    if explain_content == "Symbolic Learning":
        st.title("Symbolic Learning :pick:")
        generate_rules()
    elif explain_content == "Patient-centric Analysis":
        st.title("Patient-Centric Analysis 👨‍⚕️👩‍⚕️")
        generate_patient()
    elif explain_content == "Population-centric Analysis":
        st.title("Population-centric Analysis 👨‍👩‍👧‍👦")
        generate_population()


def app_content():
    st.title("SemDesLC")

    # Adding names of each layer
    descriptions = {
        "Deduce": "",
        "Train": "",
        "Explain": ""
    }
    colors = ['#74c69d', '#ffbf69', '#1b4965']

    labels = list(descriptions.keys())
    values = [1] * len(labels)

    # Creating the doughnut chart using plotly.js
    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=.60, marker=dict(colors=colors), pull=[0.03, 0.03, 0.03])])
    fig.update_traces(hoverinfo='label', textinfo='label', textfont_size=15,
                      marker=dict(line=dict(color=colors)))

    # Adding annotations to SemDesLC layers
    annotations = [
        dict(text='In the <b>Train layer</b>, to perform the predictive task- data quality,<br> data curation, AutoML, <br> and predictive model (e.g., Random Forest) is utilized.',
            font = dict(
            size=14,
            color="black"
            ),
            x=0.45, y=0.92, showarrow=True, bgcolor='#ffbf69', ax=-290),

        dict(text='In the <b>Explain layer</b>, symbolic learning, patient-centric and population-centric analysis <br> provides more enhanced contextual explanations <br> from a patient or population persepective.',
            font = dict(
            size=14,
            color="white"
            ),
            x=0.45, y=0.01, showarrow=True, ax=-335, bgcolor='#1b4965'),

        dict(text='In the <b>Deduce layer</b>, an interpretable tools such as Decision trees <br> and the SemDesLC KG (i.e., the traced metadata of <br> the trained predictive model) <br> provides users with reliable interpretations.',
            font=dict(
            size=14,
            color="black"
            ),
            x=0.59, y=0.60, showarrow=True, ax=230, bgcolor='#74c69d')]

    fig.update_layout(annotations=annotations, showlegend=False)

    # Displaying the chart
    st.plotly_chart(fig, use_container_width=True)


    # Sidebar for task selection
    st.sidebar.title("Go To:")

    # Initialize the key in session state
    if 'clicked' not in st.session_state:
        st.session_state.clicked = {'Train': False, 'Deduce': False, 'Explain': False}

    # Function to update the value in session state
    def clicked(button):
        st.session_state.clicked[button] = True

    col1, col2, col3, col4 = st.columns(4)
    button_width = 155
    with col1:
        button1 = st.sidebar.button("About SemDesLC")
        ChangeButtonColour('About SemDesLC', 'black', 'white', '#e5e6e4', width=button_width)
       
    with col2:
        button2 = st.sidebar.button("Train")
        ChangeButtonColour('Train', 'black', 'white', '#ffbf69', width=button_width)
        if button2:
           clicked('Train')
    with col3:
        button3 = st.sidebar.button("Deduce")
        ChangeButtonColour('Deduce', 'black', 'white', '#74c69d', width=button_width)
        if button3:
           clicked('Deduce')
    with col4:
        button4 = st.sidebar.button("Explain")
        ChangeButtonColour('Explain', 'white', 'black', '#1b4965', width=button_width)
        if button4:
           clicked('Explain')

    if button1:
        doc()

    if st.session_state.clicked.get('Train'):
        display_train()

    if st.session_state.clicked.get('Deduce'):
        display_deduce()

    if st.session_state.clicked.get('Explain'):
        display_explain()

    logout = st.sidebar.button("Logout", key="logout")
    ChangeButtonColour('Logout', 'white', 'black', '#6c757d', width=button_width)

    if logout:
        st.session_state.logged_in = False
        st.experimental_rerun()


if __name__ == "__main__":
    main_updated()