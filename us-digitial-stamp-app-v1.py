import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import uuid
import datetime

# Set page configuration
st.set_page_config(page_title="USPS Digital Stamp App", page_icon="📬", layout="wide")

# Initialize session state for user data
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'stamps' not in st.session_state:
    st.session_state.stamps = []
if 'mail_history' not in st.session_state:
    st.session_state.mail_history = []

# Directory to save stamps
STAMP_DIR = "stamps"
os.makedirs(STAMP_DIR, exist_ok=True)

# Function to create a digital stamp
def create_stamp(design, text, color, value):
    # Create a blank image
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw border based on design
    if design == "Classic":
        draw.rectangle((10, 10, 190, 190), outline=color, width=5)
    elif design == "Wavy":
        draw.rectangle((10, 10, 190, 190), outline=color, width=5)
        draw.line((20, 20, 180, 20), fill=color, width=3)
        draw.line((20, 180, 180, 180), fill=color, width=3)
    elif design == "Star":
        draw.polygon([(100, 20), (120, 80), (180, 80), (130, 120), (150, 180), 
                      (100, 140), (50, 180), (70, 120), (20, 80), (80, 80)], outline=color, width=5)
    
    # Add text (stamp value and custom text)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((20, 160), f"USPS ${value:.2f}", fill=color, font=font)
    draw.text((20, 20), text.upper(), fill=color, font=font)
    
    # Save stamp
    stamp_id = str(uuid.uuid4())
    stamp_path = os.path.join(STAMP_DIR, f"{stamp_id}.png")
    img.save(stamp_path)
    
    return stamp_id, stamp_path

# Function to simulate sending mail
def send_mail(stamp_id, recipient, address):
    mail_entry = {
        'stamp_id': stamp_id,
        'recipient': recipient,
        'address': address,
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.mail_history.append(mail_entry)

# Streamlit app
st.title("📬 USPS Digital Stamp Application")
st.write("Create, collect, and use digital stamps for your virtual mail!")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Create Stamp", "My Collection", "Send Mail", "Mail History"])

# Page 1: Create Stamp
if page == "Create Stamp":
    st.header("Create Your Digital Stamp")
    with st.form("stamp_form"):
        design = st.selectbox("Stamp Design", ["Classic", "Wavy", "Star"])
        text = st.text_input("Custom Text (e.g., Forever Stamp)", max_chars=20)
        color = st.color_picker("Stamp Color", "#0000FF")
        value = st.number_input("Stamp Value ($)", min_value=0.01, max_value=10.00, step=0.01, value=0.55)
        submitted = st.form_submit_button("Create Stamp")
        
        if submitted:
            if text.strip() == "":
                st.error("Please enter custom text.")
            else:
                # Simulate payment
                st.write("Redirecting to payment simulation...")
                if st.button("Confirm Payment"):
                    stamp_id, stamp_path = create_stamp(design, text, color, value)
                    st.session_state.stamps.append({
                        'id': stamp_id,
                        'path': stamp_path,
                        'design': design,
                        'text': text,
                        'value': value
                    })
                    st.success("Stamp created successfully!")
                    st.image(stamp_path, caption=f"Stamp: {text} (${value:.2f})", width=200)

# Page 2: My Collection
elif page == "My Collection":
    st.header("My Stamp Collection")
    if not st.session_state.stamps:
        st.info("You haven't created any stamps yet. Go to 'Create Stamp' to start!")
    else:
        cols = st.columns(3)
        for idx, stamp in enumerate(st.session_state.stamps):
            with cols[idx % 3]:
                st.image(stamp['path'], caption=f"{stamp['text']} (${stamp['value']:.2f})", width=150)
                if st.button("Delete", key=f"delete_{stamp['id']}"):
                    os.remove(stamp['path'])
                    st.session_state.stamps = [s for s in st.session_state.stamps if s['id'] != stamp['id']]
                    st.experimental_rerun()

# Page 3: Send Mail
elif page == "Send Mail":
    st.header("Send Virtual Mail")
    if not st.session_state.stamps:
        st.warning("You need to create a stamp first. Go to 'Create Stamp'!")
    else:
        with st.form("mail_form"):
            stamp = st.selectbox("Select Stamp", 
                               [(s['text'], s['id']) for s in st.session_state.stamps], 
                               format_func=lambda x: x[0])
            recipient = st.text_input("Recipient Name")
            address = st.text_area("Recipient Address")
            submitted = st.form_submit_button("Send Mail")
            
            if submitted:
                if not recipient or not address:
                    st.error("Please fill in all fields.")
                else:
                    send_mail(stamp[1], recipient, address)
                    st.success("Mail sent successfully!")
                    # Optionally remove stamp after use
                    if st.checkbox("Remove stamp after sending"):
                        stamp_data = next(s for s in st.session_state.stamps if s['id'] == stamp[1])
                        os.remove(stamp_data['path'])
                        st.session_state.stamps = [s for s in st.session_state.stamps if s['id'] != stamp[1]]

# Page 4: Mail History
elif page == "Mail History":
    st.header("Mail History")
    if not st.session_state.mail_history:
        st.info("No mail sent yet. Go to 'Send Mail' to start!")
    else:
        for mail in st.session_state.mail_history:
            stamp_data = next((s for s in st.session_state.stamps if s['id'] == mail['stamp_id']), None)
            st.write("---")
            st.write(f"**Sent to**: {mail['recipient']}")
            st.write(f"**Address**: {mail['address']}")
            st.write(f"**Date**: {mail['date']}")
            if stamp_data:
                st.image(stamp_data['path'], caption=f"Stamp: {stamp_data['text']}", width=100)
            else:
                st.write("Stamp no longer available.")
