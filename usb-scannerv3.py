import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(page_title="USB Barcode Scanner App", layout="centered")

# App title
st.title("USB Barcode Scanner Application")
st.write("Scan a barcode using your USB scanner and see the results below.")

# Initialize session state variables
if "scanned_barcodes" not in st.session_state:
    st.session_state.scanned_barcodes = []

if "current_barcode" not in st.session_state:
    st.session_state.current_barcode = ""  # Keep the current barcode value in session state

# JavaScript to maintain focus on the barcode input field
focus_script = """
    <script>
        const inputField = document.getElementById("barcode_input");
        if (inputField) {
            inputField.focus();
            inputField.addEventListener("blur", () => {
                inputField.focus(); // Refocus if the input field loses focus
            });
        }
    </script>
"""

# Barcode input field
barcode = st.text_input(
    "Scan your barcode here:",
    value=st.session_state.current_barcode,
    key="barcode_input",
    placeholder="Scan your barcode here...",
    label_visibility="hidden",  # Optional: hide label to reduce redundancy
)

# Inject JavaScript to maintain focus
st.markdown(focus_script, unsafe_allow_html=True)

# When a barcode is entered
if barcode and barcode != st.session_state.current_barcode:
    # Record the scanned barcode with a timestamp
    scanned_data = {
        "barcode": barcode.strip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.scanned_barcodes.append(scanned_data)

    # Display a success message
    st.success(f"Scanned barcode: {barcode}")

    # Save the new barcode in session state
    st.session_state.current_barcode = barcode

# Display the scanned barcodes
if st.session_state.scanned_barcodes:
    st.subheader("Scanned Barcodes")
    for i, data in enumerate(st.session_state.scanned_barcodes, start=1):
        st.write(f"**{i}. Barcode:** {data['barcode']} (Scanned at: {data['timestamp']})")

# Button to clear scanned data
if st.button("Clear Scanned Barcodes"):
    st.session_state.scanned_barcodes = []
    st.session_state.current_barcode = ""  # Reset the barcode input value
    st.experimental_rerun()  # Trigger rerun to reset the state

# Footer
st.markdown("---")
st.write("Developed using Streamlit. Ensure your USB barcode scanner is working as a keyboard input device.")
