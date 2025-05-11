import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import uuid
import datetime

# Set page configuration
st.set_page_config(page_title="USPS Physical Stamp App", page_icon="📬", layout="wide")

# Initialize session state for user data
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'stamps' not in st.session_state:
    st.session_state.stamps = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Directory to save stamp designs
STAMP_DIR = "stamps"
os.makedirs(STAMP_DIR, exist_ok=True)

# Function to create a stamp design
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
    
    # Save stamp design
    stamp_id = str(uuid.uuid4())
    stamp_path = os.path.join(STAMP_DIR, f"{stamp_id}.png")
    img.save(stamp_path)
    
    return stamp_id, stamp_path

# Function to place an order
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
        return total_cost
    return 0

# Streamlit app
st.title("📬 USPS Physical Stamp Application")
st.write("Design and order custom physical stamps for your mailing needs!")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Create Stamp", "My Collection", "Order Stamps", "Order History"])

# Page 1: Create Stamp
if page == "Create Stamp":
    st.header("Create Your Custom Stamp Design")
    with st.form("stamp_form"):
        design = st.selectbox("Stamp Design", ["Classic", "Wavy", "Star"])
        text = st.text_input("Custom Text (e.g., Forever Stamp)", max_chars=20)
        color = st.color_picker("Stamp Color", "#0000FF")
        value = st.number_input("Stamp Value ($)", min_value=0.01, max_value=10.00, step=0.01, value=0.55)
        submitted = st.form_submit_button("Create Stamp Design")
        
        if submitted:
            if text.strip() == "":
                st.error("Please enter custom text.")
            else:
                # Simulate design approval
                st.write("Submitting design for USPS approval...")
                if st.button("Confirm Design"):
                    stamp_id, stamp_path = create_stamp(design, text, color, value)
                    st.session_state.stamps.append({
                        'id': stamp_id,
                        'path': stamp_path,
                        'design': design,
                        'text': text,
                        'value': value
                    })
                    st.success("Stamp design created successfully!")
                    st.image(stamp_path, caption=f"Stamp: {text} (${value:.2f})", width=200)

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
                    st.experimental_rerun()

# Page 3: Order Stamps
elif page == "Order Stamps":
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
                    # Simulate payment
                    total_cost = place_order(stamp[1], quantity, shipping_address)
                    if total_cost > 0:
                        stamp_data = next(s for s in st.session_state.stamps if s['id'] == stamp[1])
                        st.write(f"Total Cost: ${total_cost:.2f} for {quantity} stamps")
                        if st.button("Confirm Payment"):
                            st.success(f"Order placed for {quantity} stamps! Check 'Order History' for details.")
                    else:
                        st.error("Error processing order. Try again.")

# Page 4: Order History
elif page == "Order History":
    st.header("Order History")
    if not st.session_state.orders:
        st.info("No orders placed yet. Go to 'Order Stamps' to start!")
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
