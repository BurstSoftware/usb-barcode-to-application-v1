import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(page_title="USB Barcode Scanner App", layout="centered")

# App title
st.title("USB Barcode Scanner Application")
st.write("Scan a barcode using your USB scanner and see the results below.")

# Initialize session state
if "scanned_barcodes" not in st.session_state:
    st.session_state.scanned_barcodes = []

# Text input for barcode with autofocus
barcode = st.text_input(
    "Scan your barcode here:",
    value="",  # Empty input field
    key="barcode_input",
    placeholder="Waiting for barcode...",
    label_visibility="visible",
    help="Focus remains here for next scan.",
    max_chars=100,
    type="default",
    autofocus=True,  # Ensures the cursor focuses on this field
)

if barcode:
    # Record the scanned barcode with a timestamp (no duplicate check)
    scanned_data = {
        "barcode": barcode.strip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.scanned_barcodes.append(scanned_data)

    # Display a success message
    st.success(f"Scanned barcode: {barcode}")

    # Clear the input field by resetting the text_input value
    st.experimental_set_query_params(barcode_input="")  # Query param hack to clear the field

# Display the scanned barcodes
if st.session_state.scanned_barcodes:
    st.subheader("Scanned Barcodes")
    for i, data in enumerate(st.session_state.scanned_barcodes, start=1):
        st.write(f"**{i}. Barcode:** {data['barcode']} (Scanned at: {data['timestamp']})")

# Provide an option to clear the scanned data
if st.button("Clear Scanned Barcodes"):
    st.session_state.scanned_barcodes = []
    st.experimental_set_query_params(barcode_input="")  # Query param hack
    st.experimental_rerun()  # Trigger rerun to reset the state

# Footer
st.markdown("---")
st.write("Developed using Streamlit. Ensure your USB barcode scanner is working as a keyboard input device.")
