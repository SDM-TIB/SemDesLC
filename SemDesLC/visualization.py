import streamlit as st
from InterpretME import plots
from PIL import Image
from streamlit.components.v1 import html


def render_svg(svg_string):
    """Renders the given svg string."""
    c = st.container()
    with c:
        html(svg_string,width=700, height=700, scrolling=True)

def display_image(image_file):
    img = Image.open(image_file)
    st.image(img, caption='Feature Importance', use_column_width=True)



def feature_importance():

    if st.button("Feature Importance"):
        fm = plots.feature_importance(results=st.session_state.results, path=st.session_state.path_results)
        st.write(fm)
        st.success("Storing plot at given path")
        display_image(fm)

def decision_trees():

    if st.button("Decision Tree"):
        dt = plots.decision_trees(results=st.session_state.results, path=st.session_state.path_results)
        st.write(dt)
        st.success("Storing plot at given path")
        render_svg(open(dt).read())

def constraint_decision_trees():

    if st.button("Constraint Decision Tree"):
        cdt = plots.constraints_decision_trees(results=st.session_state.results, path=st.session_state.path_results, constraint_num=[1])
        st.write(cdt)
        st.success("Storing plot at given path")
        render_svg(open(cdt).read())

def visualization():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Feature Importance Plot")
        feature_importance()
    with col2:
        st.header("Decision Tree")
        decision_trees()
    with col3:
        st.header("Constraint Decision Tree")
        constraint_decision_trees()