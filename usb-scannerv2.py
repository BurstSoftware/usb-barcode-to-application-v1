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

if "input_key" not in st.session_state:
    st.session_state.input_key = 0  # Unique key for text input to reset it

# Temporary variable to store barcode input
barcode = st.text_input("Scan your barcode here:", key=f"barcode_input_{st.session_state.input_key}")

if barcode:
    # Check if the barcode has already been scanned
    if barcode not in [data["barcode"] for data in st.session_state.scanned_barcodes]:
        # Record the scanned barcode with a timestamp
        scanned_data = {
            "barcode": barcode.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        st.session_state.scanned_barcodes.append(scanned_data)

        # Display a success message
        st.success(f"Scanned barcode: {barcode}")

        # Increment the input key to reset the text input field
        st.session_state.input_key += 1
        st.experimental_rerun()  # Trigger rerun to reset input field
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
    st.session_state.input_key += 1  # Reset the input field key
    st.experimental_rerun()  # Trigger rerun to reset the state

# Footer
st.markdown("---")
st.write("Developed using Streamlit. Ensure your USB barcode scanner is working as a keyboard input device.")
