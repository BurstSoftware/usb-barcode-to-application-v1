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

# JavaScript to keep the focus on the text input field
focus_script = """
    <script>
        // Automatically focus on the input field when the page is loaded or rerun
        document.getElementById("barcode_input").focus();
    </script>
"""

# Temporary variable to store barcode input
barcode = st.text_input(
    "Scan your barcode here:",
    key=f"barcode_input_{st.session_state.input_key}",
    label_visibility="hidden",  # Hides the label to prevent duplication
    placeholder="Scan your barcode here...",
)

# Inject JavaScript for autofocus
st.markdown(focus_script, unsafe_allow_html=True)

if barcode:
    # Record the scanned barcode with a timestamp (no duplicate check)
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
