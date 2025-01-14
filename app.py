import streamlit as st
import numpy as np

def calculate_next_vr_gcr(current_vessels, new_vessels_count, target_weighted_vr, target_weighted_gcr):
    total_discharge_loading = sum(v['discharge'] + v['loading'] for v in current_vessels)
    total_operational_hours = sum(v['operational_hours'] for v in current_vessels)
    total_qc_working_hours = sum(v['qc_working_hours'] for v in current_vessels)

    target_total_discharge_loading_vr = target_weighted_vr * (total_operational_hours + new_vessels_count)
    target_total_discharge_loading_gcr = target_weighted_gcr * (total_qc_working_hours + new_vessels_count)

    target_total_discharge_loading = max(
        target_total_discharge_loading_vr, target_total_discharge_loading_gcr
    )

    new_vessels_discharge_loading = target_total_discharge_loading - total_discharge_loading

    avg_operational_hours_new = new_vessels_discharge_loading / target_weighted_vr
    avg_qc_working_hours_new = new_vessels_discharge_loading / target_weighted_gcr

    avg_vr = new_vessels_discharge_loading / avg_operational_hours_new
    avg_gcr = new_vessels_discharge_loading / avg_qc_working_hours_new

    return {
        'average_vr': avg_vr,
        'average_gcr': avg_gcr,
        'new_vessels_discharge_loading': new_vessels_discharge_loading / new_vessels_count
    }

# Streamlit app
st.title("VR and GCR Target Calculator")

# Input data
st.subheader("Existing Vessels Data")
current_vessels = [
    {'discharge': 763, 'loading': 639, 'operational_hours': 14.9, 'qc_working_hours': 39.8},
    {'discharge': 564, 'loading': 784, 'operational_hours': 14.9, 'qc_working_hours': 47.0},
    {'discharge': 555, 'loading': 760, 'operational_hours': 16.8, 'qc_working_hours': 43.3},
    {'discharge': 705, 'loading': 365, 'operational_hours': 15.9, 'qc_working_hours': 37.4},
    {'discharge': 0, 'loading': 856, 'operational_hours': 12.1, 'qc_working_hours': 38.7},
    {'discharge': 683, 'loading': 788, 'operational_hours': 12.7, 'qc_working_hours': 38.4}
]

new_vessels_count = st.number_input("Number of New Vessels", min_value=1, step=1, value=3)
target_weighted_vr = st.number_input("Target Weighted VR", value=90.0)
target_weighted_gcr = st.number_input("Target Weighted GCR", value=32.0)

# Calculation button
if st.button("Calculate"):
    result = calculate_next_vr_gcr(current_vessels, new_vessels_count, target_weighted_vr, target_weighted_gcr)

    st.subheader("Results")
    st.write("Average VR for New Vessels:", result['average_vr'])
    st.write("Average GCR for New Vessels:", result['average_gcr'])
    st.write("Average Discharge + Loading per New Vessel:", result['new_vessels_discharge_loading'])
