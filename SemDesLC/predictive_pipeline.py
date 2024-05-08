import streamlit as st
import time
from InterpretME import pipeline


def main_process():

    st.header("Use Case: Lung Cancer Relapse Prediction")
    st.write("This an example on how SemDesLC can be used to interpret the prediction and trace back a particular target entity. The Lung Cancer Benchmark is a fully curated subset of Bio-medical domain, describes a lung cancer patient with medical characteristics such as smoking habit, ID, gender, age, biomarker, relapse etc. Here, the predictive task is a binary classification to predict whether a patient have `Relapse`")

    st.header("Predictive Modeling :computer:")

    # Create a file upload widget for the input JSON file
    uploaded_file = st.file_uploader("Upload a input config file", type=["json"])

    # Allow the user to specify an output path for saving the results
    st.session_state.path_results = st.text_input("Enter the path to store results")


    # Create a button for running pipeline
    if st.button("Run SemDesLC Pipeline"):
        if uploaded_file is not None:
            if st.session_state.path_results:
                # Get the paths from the user input
                input_path = uploaded_file.name

                # Create progress bar
                progress_text = "SemDesLC pipeline execution in progress. Please wait."
                progress_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                # Run InterpretME pipeline function
                st.session_state.results = pipeline(path_config=input_path, lime_results=st.session_state.path_results)
                progress_bar.empty()

                st.write(st.session_state.results)
                # Display the results
                st.write("Processing result:")
                st.success(f"Result saved to {st.session_state.path_results}")

            else:
                st.error("Please specify an output file path.")
        else:
            st.error("Please upload a input JSON file.")

if __name__ == "__main__":
    main_process()