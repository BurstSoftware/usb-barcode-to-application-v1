USB Barcode Scanner Application
This is a simple USB Barcode Scanner Application developed using Streamlit. It allows users to scan barcodes using a USB barcode scanner (or manual input) and displays the scanned results in real time.

Features
Real-Time Scanning: Scans and logs barcodes instantly as they are input.
Duplicate-Friendly: Allows the same barcode to be scanned multiple times, displaying each instance with a timestamp.
Clearing Input: Automatically clears the input field after a barcode is scanned, improving usability.
Scanned History: Displays all scanned barcodes with the corresponding timestamps.
Clear Scanned Barcodes: Users can clear the scanned barcode history with a button.
Prerequisites
Ensure the following dependencies are installed:

Python 3.8 or later
Streamlit
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-repo-name/usb-barcode-scanner-app.git
cd usb-barcode-scanner-app
Create a Virtual Environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Running the Application
To launch the Streamlit application, run:

bash
Copy code
streamlit run app.py
Replace app.py with the filename containing the code (e.g., main.py or usb_scanner_app.py).

How to Use
Launch the App: Open the app using the above command.
Scan a Barcode:
Place the cursor in the text input field labeled "Scan your barcode here:".
Use a USB barcode scanner to scan barcodes, or type them manually and hit Enter.
View Scanned Barcodes:
All scanned barcodes will be displayed in the "Scanned Barcodes" section with timestamps.
Duplicate barcodes will be recorded and displayed as separate entries.
Clear Scanned Barcodes:
Click on the "Clear Scanned Barcodes" button to clear the scanned history.
Example
After scanning barcodes, the app will display:

yaml
Copy code

Scanned Barcodes
1. Barcode: 123456789 (Scanned at: 2024-06-16 12:00:00)
2. Barcode: 123456789 (Scanned at: 2024-06-16 12:00:05)
3. Barcode: 987654321 (Scanned at: 2024-06-16 12:01:10)

Code Overview

Session State: Used to persist scanned barcodes and reset the input field.
Text Input Reset: Implemented using a unique key (input_key) and st.experimental_rerun() to clear the input field.
Dynamic UI: Displays scanned barcodes dynamically and timestamps them.
Dependencies
Streamlit: Web app framework for Python.
Python >=3.8: Base requirement.
Requirements File
Example requirements.txt:

plaintext
Copy code
streamlit>=1.10.0
Install dependencies using:

bash
Copy code
pip install -r requirements.txt
Customization
To add input validation or barcode format restrictions, modify the barcode input logic.
To prevent duplicates, reintroduce a check before appending to the session state list.
Troubleshooting
Input Field Not Clearing: Ensure st.experimental_rerun() is used after incrementing the input key.
Session State Issues: Double-check initialization of scanned_barcodes and input_key in st.session_state.
Contributing
Fork the repository.
Create a new branch: git checkout -b feature-name.
Commit changes: git commit -m "Add new feature".
Push the branch: git push origin feature-name.
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.
