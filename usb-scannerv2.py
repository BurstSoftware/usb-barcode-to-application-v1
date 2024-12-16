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

# Input field to capture barcode data
barcode = st.text_input("Scan your barcode here:", key="barcode_input")

if barcode:
    # Check if the barcode has already been scanned
    if barcode not in [data["barcode"] for data in st.session_state.scanned_barcodes]:
        # Record the scanned barcode with a timestamp
        scanned_data = {
            "barcode": barcode,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.scanned_barcodes.append(scanned_data)

        # Display a success message
        st.success(f"Scanned barcode: {barcode}")

        # Clear the input field after successful scan
        st.session_state.barcode_input = ""
        st.experimental_rerun()  # Refresh the app to reflect the cleared input
    else:
        st.warning("You have already scanned this barcode.")

# Display the scanned barcodes
if st.session_state.scanned_barcodes:
    st.subheader("Scanned Barcodes")
    for i, data in enumerate(st.session_state.scanned_barcodes, start=1):
        st.write(f"**{i}. Barcode:** {data['barcode']} (Scanned at: {data['timestamp']})")

# Provide an option to clear the scanned data
if st.button("Clear Scanned Barcodes"):
    st.session_state.scanned_barcodes = []
    st.success("Scanned barcodes cleared!")
    st.experimental_rerun()  # Refresh the app to reset the state

# Footer
st.markdown("---")
st.write("Developed using Streamlit. Ensure your USB barcode scanner is working as a keyboard input device.")
