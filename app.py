import pandas as pd
import streamlit as st

def calculate_next_vr_gcr(
    current_vessels,
    new_vessels,
    target_weighted_vr,
    target_weighted_gcr,
    avg_crane_performance,
    avg_qc_factor
):
    # Calculate current totals
    total_discharge_loading = current_vessels['discharge'].sum() + current_vessels['loading'].sum()
    total_operational_hours = current_vessels['operational_hours'].sum()
    total_qc_working_hours = current_vessels['qc_working_hours'].sum()

    # Estimate operational and QC hours for new vessels
    new_vessels['operational_hours'] = (new_vessels['discharge'] + new_vessels['loading']) / (
        new_vessels['crane_intensity'] * avg_crane_performance
    )
    new_vessels['qc_working_hours'] = new_vessels['operational_hours'] * avg_qc_factor

    # Add new vessels data to totals
    total_discharge_loading += new_vessels['discharge'].sum() + new_vessels['loading'].sum()
    total_operational_hours += new_vessels['operational_hours'].sum()
    total_qc_working_hours += new_vessels['qc_working_hours'].sum()

    # Calculate Weighted VR and GCR
    weighted_vr = total_discharge_loading / total_operational_hours
    weighted_gcr = total_discharge_loading / total_qc_working_hours

    return {
        'weighted_vr': weighted_vr,
        'weighted_gcr': weighted_gcr,
        'new_vessels_data': new_vessels
    }

# Streamlit app
st.title("VR and GCR Target Calculator")

# Upload existing vessel data
st.subheader("Upload Existing Vessel Data")
existing_file = st.file_uploader("Upload an XLSX file for existing vessels", type="xlsx")
if existing_file:
    current_vessels = pd.read_excel(existing_file)
    st.write("Existing Vessel Data:", current_vessels)
else:
    st.warning("Please upload an XLSX file with columns: discharge, loading, operational_hours, qc_working_hours.")

# Upload new vessel data
st.subheader("Upload New Vessel Data")
new_file = st.file_uploader("Upload an XLSX file for new vessels", type="xlsx")
if new_file:
    new_vessels = pd.read_excel(new_file)
    st.write("New Vessel Data:", new_vessels)
else:
    st.warning("Please upload an XLSX file with columns: discharge, loading, crane_intensity.")

# Input target values
target_weighted_vr = st.number_input("Target Weighted VR", value=90.0)
target_weighted_gcr = st.number_input("Target Weighted GCR", value=32.0)

if existing_file and new_file:
    # Calculate averages from current vessels
    avg_crane_performance = (current_vessels['discharge'] + current_vessels['loading']).sum() / (
        current_vessels['operational_hours'] * current_vessels['crane_intensity']
    ).sum()
    avg_qc_factor = (current_vessels['qc_working_hours'] / current_vessels['operational_hours']).mean()

    # Calculate required VR and GCR for new vessels
    result = calculate_next_vr_gcr(
        current_vessels, new_vessels, target_weighted_vr, target_weighted_gcr, avg_crane_performance, avg_qc_factor
    )

    st.subheader("Results")
    st.write("Weighted VR after adding new vessels:", result['weighted_vr'])
    st.write("Weighted GCR after adding new vessels:", result['weighted_gcr'])
    st.write("Estimated Data for New Vessels:", result['new_vessels_data'])
