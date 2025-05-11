import streamlit as st
import os
import json
import uuid
import datetime
from PIL import Image, ImageDraw, ImageFont

# Set page configuration
st.set_page_config(page_title="USPS Stamp App", page_icon="📬", layout="wide")

# Directories for stamps and data
STAMP_DIR = "stamps"
DATA_FILE = "data.json"
os.makedirs(STAMP_DIR, exist_ok=True)

# Function to load data from JSON file
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {'stamps': [], 'mail_history': [], 'orders': []}
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {'stamps': [], 'mail_history': [], 'orders': []}

# Function to save data to JSON file
def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Initialize session state and load persisted data
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'stamp_stage' not in st.session_state:
    st.session_state.stamp_stage = "input"  # Stages: input, preview, confirmed
if 'pending_stamp' not in st.session_state:
    st.session_state.pending_stamp = None

# Load data into session state
data = load_data()
if 'stamps' not in st.session_state:
    st.session_state.stamps = data.get('stamps', [])
if 'mail_history' not in st.session_state:
    st.session_state.mail_history = data.get('mail_history', [])
if 'orders' not in st.session_state:
    st.session_state.orders = data.get('orders', [])

# Function to create a stamp design
def create_stamp(design, text, color, value):
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    if design == "Classic":
        draw.rectangle((10, 10, 190, 190), outline=color, width=5)
    elif design == "Wavy":
        draw.rectangle((10, 10, 190, 190), outline=color, width=5)
        draw.line((20, 20, 180, 20), fill=color, width=3)
        draw.line((20, 180, 180, 180), fill=color, width=3)
    elif design == "Star":
        draw.polygon([(100, 20), (120, 80), (180, 80), (130, 120), (150, 180), 
                      (100, 140), (50, 180), (70, 120), (20, 80), (80, 80)], outline=color, width=5)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((20, 160), f"USPS ${value:.2f}", fill=color, font=font)
    draw.text((20, 20), text.upper(), fill=color, font=font)
    
    stamp_id = str(uuid.uuid4())
    stamp_path = os.path.join(STAMP_DIR, f"{stamp_id}.png")
    img.save(stamp_path)
    
    return stamp_id, stamp_path

# Function to send virtual mail
def send_mail(stamp_id, recipient, address):
    mail_entry = {
        'stamp_id': stamp_id,
        'recipient': recipient,
        'address': address,
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.mail_history.append(mail_entry)
    save_data({
        'stamps': st.session_state.stamps,
        'mail_history': st.session_state.mail_history,
        'orders': st.session_state.orders
    })

# Function to place an order for physical stamps
def place_order(stamp_id, quantity, shipping_address):
    stamp_data = next((s for s in st.session_state.stamps if s['id'] == stamp_id), None)
    if stamp_data:
        total_cost = stamp_data['value'] * quantity
        order_entry = {
            'order_id': str(uuid.uuid4()),
            'stamp_id': stamp_id,
            'quantity': quantity,
            'total_cost': total_cost,
            'shipping_address': shipping_address,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.orders.append(order_entry)
        save_data({
            'stamps': st.session_state.stamps,
            'mail_history': st.session_state.mail_history,
            'orders': st.session_state.orders
        })
        return total_cost
    return 0

# Streamlit app
st.title("📬 USPS Stamp Application")
st.write("Design, use, and order custom stamps for digital and physical mailing!")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Create Stamp", "My Collection", "Send Virtual Mail", "Order Physical Stamps", "History"])

# Page 1: Create Stamp
if page == "Create Stamp":
    st.header("Create Your Custom Stamp Design")
    with st.form("stamp_form", clear_on_submit=False):
        design = st.selectbox("Stamp Design", ["Classic", "Wavy", "Star"], key="design_select")
        text = st.text_input("Custom Text (e.g., Forever Stamp)", max_chars=20, key="text_input")
        color = st.color_picker("Stamp Color", "#0000FF", key="color_picker")
        value = st.number_input("Stamp Value ($)", min_value=0.01, max_value=10.00, step=0.01, value=0.55, key="value_input")
        
        button_label = "Preview Stamp Design" if st.session_state.stamp_stage == "input" else "Confirm Design"
        submitted = st.form_submit_button(button_label)
        
        if submitted:
            if text.strip() == "":
                st.error("Please enter custom text.")
            elif st.session_state.stamp_stage == "input":
                st.session_state.pending_stamp = {
                    'design': design,
                    'text': text,
                    'color': color,
                    'value': value
                }
                st.session_state.stamp_stage = "preview"
                st.write("Preview your stamp design below. Submit again to confirm.")
                temp_stamp_id, temp_stamp_path = create_stamp(design, text, color, value)
                st.image(temp_stamp_path, caption=f"Preview: {text} (${value:.2f})", width=200)
                os.remove(temp_stamp_path)
            elif st.session_state.stamp_stage == "preview":
                st.session_state.stamp_stage = "confirmed"
        
        if st.session_state.stamp_stage == "confirmed" and st.session_state.pending_stamp:
            stamp_id, stamp_path = create_stamp(
                st.session_state.pending_stamp['design'],
                st.session_state.pending_stamp['text'],
                st.session_state.pending_stamp['color'],
                st.session_state.pending_stamp['value']
            )
            st.session_state.stamps.append({
                'id': stamp_id,
                'path': stamp_path,
                'design': st.session_state.pending_stamp['design'],
                'text': st.session_state.pending_stamp['text'],
                'value': st.session_state.pending_stamp['value']
            })
            save_data({
                'stamps': st.session_state.stamps,
                'mail_history': st.session_state.mail_history,
                'orders': st.session_state.orders
            })
            st.success("Stamp design created successfully!")
            st.image(stamp_path, caption=f"Stamp: {st.session_state.pending_stamp['text']} (${st.session_state.pending_stamp['value']:.2f})", width=200)
            st.session_state.stamp_stage = "input"
            st.session_state.pending_stamp = None

# Page 2: My Collection
elif page == "My Collection":
    st.header("My Stamp Designs")
    if not st.session_state.stamps:
        st.info("You haven't created any stamp designs yet. Go to 'Create Stamp' to start!")
    else:
        cols = st.columns(3)
        for idx, stamp in enumerate(st.session_state.stamps):
            with cols[idx % 3]:
                st.image(stamp['path'], caption=f"{stamp['text']} (${stamp['value']:.2f})", width=150)
                if st.button("Delete", key=f"delete_{stamp['id']}"):
                    os.remove(stamp['path'])
                    st.session_state.stamps = [s for s in st.session_state.stamps if s['id'] != stamp['id']]
                    save_data({
                        'stamps': st.session_state.stamps,
                        'mail_history': st.session_state.mail_history,
                        'orders': st.session_state.orders
                    })
                    st.experimental_rerun()

# Page 3: Send Virtual Mail
elif page == "Send Virtual Mail":
    st.header("Send Virtual Mail")
    if not st.session_state.stamps:
        st.warning("You need to create a stamp design first. Go to 'Create Stamp'!")
    else:
        with st.form("mail_form"):
            stamp = st.selectbox("Select Stamp Design", 
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
                    st.success("Virtual mail sent successfully!")
                    if st.checkbox("Remove stamp after sending"):
                        stamp_data = next(s for s in st.session_state.stamps if s['id'] == stamp[1])
                        os.remove(stamp_data['path'])
                        st.session_state.stamps = [s for s in st.session_state.stamps if s['id'] != stamp[1]]
                        save_data({
                            'stamps': st.session_state.stamps,
                            'mail_history': st.session_state.mail_history,
                            'orders': st.session_state.orders
                        })

# Page 4: Order Physical Stamps
elif page == "Order Physical Stamps":
    st.header("Order Physical Stamps")
    if not st.session_state.stamps:
        st.warning("You need to create a stamp design first. Go to 'Create Stamp'!")
    else:
        with st.form("order_form"):
            stamp = st.selectbox("Select Stamp Design", 
                               [(s['text'], s['id']) for s in st.session_state.stamps], 
                               format_func=lambda x: x[0])
            quantity = st.number_input("Number of Stamps Needed", min_value=1, max_value=1000, step=1, value=1)
            shipping_address = st.text_area("Shipping Address")
            submitted = st.form_submit_button("Place Order")
            
            if submitted:
                if not shipping_address:
                    st.error("Please provide a shipping address.")
                else:
                    total_cost = place_order(stamp[1], quantity, shipping_address)
                    if total_cost > 0:
                        stamp_data = next(s for s in st.session_state.stamps if s['id'] == stamp[1])
                        st.write(f"Total Cost: ${total_cost:.2f} for {quantity} stamps")
                        if st.button("Confirm Payment", key=f"confirm_payment_{stamp[1]}"):
                            st.success(f"Order placed for {quantity} stamps! Check 'History' for details.")
                    else:
                        st.error("Error processing order. Try again.")

# Page 5: History (Combined Mail and Order History)
elif page == "History":
    st.header("History")
    
    st.subheader("Virtual Mail History")
    if not st.session_state.mail_history:
        st.info("No virtual mail sent yet. Go to 'Send Virtual Mail' to start!")
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
                st.write("Stamp design no longer available.")
    
    st.subheader("Physical Stamp Order History")
    if not st.session_state.orders:
        st.info("No orders placed yet. Go to 'Order Physical Stamps' to start!")
    else:
        for order in st.session_state.orders:
            stamp_data = next((s for s in st.session_state.stamps if s['id'] == order['stamp_id']), None)
            st.write("---")
            st.write(f"**Order ID**: {order['order_id']}")
            st.write(f"**Quantity**: {order['quantity']} stamps")
            st.write(f"**Total Cost**: ${order['total_cost']:.2f}")
            st.write(f"**Shipping Address**: {order['shipping_address']}")
            st.write(f"**Date**: {order['date']}")
            if stamp_data:
                st.image(stamp_data['path'], caption=f"Stamp: {stamp_data['text']}", width=100)
            else:
                st.write("Stamp design no longer available.")
