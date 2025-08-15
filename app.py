import streamlit as st
import os
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.vectors import StrVector

# --- R setup ---
@st.cache_resource
def setup_r_environment():
    """Sets up the R environment and returns the visualization function."""
    # Activate the pandas to R data frame conversion
    pandas2ri.activate()

    # Import R's 'source' function and 'data' function
    r_source = ro.r['source']
    r_data = ro.r['data']

    # Source the R script
    r_source('scripts/visualize_pathway.R')

    # Get the R function
    visualize_kegg_pathway_r = ro.globalenv['visualize_kegg_pathway']

    # Load KEGG pathway data and get pathway names
    kegg_gs = r_data('kegg.gs')
    pathway_names = ro.r['names'](kegg_gs)

    return visualize_kegg_pathway_r, list(pathway_names)

try:
    visualize_kegg_pathway_r, pathway_names = setup_r_environment()
except Exception as e:
    st.error(f"Failed to set up R environment: {e}")
    st.stop()


# --- Streamlit App ---
st.title("OSDR Pathway Visualizer")

study_id = st.text_input("Enter OSDR Study ID (e.g., OSD-123):")
pathway_name = st.selectbox("Select a KEGG Pathway:", pathway_names)

if st.button("Visualize Pathway"):
    if study_id and pathway_name:
        with st.spinner(f"Fetching data for study {study_id} and visualizing pathway..."):
            try:
                st.write(f"Fetching data for study: {study_id}")

                # Placeholder for API call and data processing
                st.write("Calling OSDR API... (placeholder)")
                # In a real app, you would call the API here and get gene expression data

                # Dummy data
                gene_data = {
                    '5649': -3.697769, # RELN
                    '891': -7.398862, # CCNB1
                    '8519': 8.852879, # IFITM1
                    '3269': -6.379446  # HRH1
                }

                pathway_id = pathway_name.split(" ")[0]
                output_file = f"{pathway_id}.png"

                st.write(f"Visualizing pathway: {pathway_name}")

                # Convert python dict to R named vector
                r_expression_data = ro.FloatVector(list(gene_data.values()))
                r_expression_data.names = StrVector(list(gene_data.keys()))

                # Call the R function
                result = visualize_kegg_pathway_r(r_expression_data, pathway_id, output_file)

                st.success(result[0])

                if os.path.exists(output_file):
                    st.image(output_file)
                else:
                    st.error("Pathway image could not be generated.")

            except Exception as e:
                st.error(f"An error occurred during pathway visualization: {e}")

    else:
        st.warning("Please enter a study ID and select a pathway.")
