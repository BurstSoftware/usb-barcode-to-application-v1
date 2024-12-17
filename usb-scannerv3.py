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

# JavaScript to maintain focus and clear the input field dynamically
focus_script = """
<script>
    // Ensure the input field remains focused
    function maintainFocus() {
        const inputField = document.getElementById("barcode_input");
        if (inputField) {
            inputField.focus();
            inputField.addEventListener("blur", () => {
                inputField.focus(); // Refocus if the input field loses focus
            });
        }
    }

    // Clear the input field after a scan
    function clearInput() {
        const inputField = document.getElementById("barcode_input");
        if (inputField) {
            inputField.value = ""; // Clear input value
        }
    }

    // Run focus maintenance on page load
    document.addEventListener("DOMContentLoaded", maintainFocus);
    maintainFocus();

    // Expose the clearInput function globally for Streamlit
    window.clearInput = clearInput;
</script>
"""

# Barcode input field
barcode = st.text_input(
    "Scan your barcode here:",
    key="barcode_input",
    placeholder="Scan your barcode here...",
    label_visibility="hidden",  # Optional: hide label to reduce redundancy
)

# Inject JavaScript for focus management and input clearing
st.markdown(focus_script, unsafe_allow_html=True)

if barcode:
    # Record the scanned barcode with a timestamp
    scanned_data = {
        "barcode": barcode.strip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.scanned_barcodes.append(scanned_data)

    # Display a success message
    st.success(f"Scanned barcode: {barcode}")

    # Clear the input field via JavaScript
    st.markdown(
        """<script>clearInput();</script>""",
        unsafe_allow_html=True,
    )

# Display the scanned barcodes
if st.session_state.scanned_barcodes:
    st.subheader("Scanned Barcodes")
    for i, data in enumerate(st.session_state.scanned_barcodes, start=1):
        st.write(f"**{i}. Barcode:** {data['barcode']} (Scanned at: {data['timestamp']})")

# Button to clear scanned data
if st.button("Clear Scanned Barcodes"):
    st.session_state.scanned_barcodes = []
    st.experimental_rerun()  # Trigger rerun to reset the state

# Footer
st.markdown("---")
st.write("Developed using Streamlit. Ensure your USB barcode scanner is working as a keyboard input device.")
