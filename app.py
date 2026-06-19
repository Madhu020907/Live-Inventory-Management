import streamlit as st
import requests

# Point this to your live running FastAPI backend server URL
BACKEND_URL = "http://127.0.0.1:8000/products"

st.set_page_config(page_title="E-Commerce Dashboard", layout="centered")

# --- CUSTOM VISUAL STYLING (CSS) ---
st.markdown(
    """
    <style>
    /* 1. Set a background image for the main app area */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.85)), 
                          url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* 2. Style the main header font and glowing color */
    h1 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #00ffcc !important;
        text-shadow: 0px 0px 15px rgba(0, 255, 204, 0.6);
        font-weight: 800 !important;
    }
    
    /* 3. Style the secondary headers */
    h3 {
        font-family: 'Segoe UI', sans-serif !important;
        color: #ff007f !important;
        font-weight: 600 !important;
    }

    /* 4. Make the input form cards slightly transparent with a neon border */
    div[data-testid="stForm"] {
        background-color: rgba(20, 20, 30, 0.8) !important;
        border: 1px solid #ff007f !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 20px rgba(255, 0, 127, 0.2);
    }

    /* 5. Style the inventory display row containers */
    div.element-container:has(div.stMarkdown) {
        font-family: 'Consolas', monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛒 E-Commerce Inventory Dashboard")
st.write("Manage your SQL database inventory live using this styled panel.")

# --- SECTION 1: ADD NEW PRODUCT FORM ---
st.subheader("➕ Add New Inventory Item")
with st.form("add_product_form", clear_on_submit=True):
    name = st.text_input("Product Name", placeholder="e.g., Gaming Keyboard")
    price = st.number_input("Price (₹)", min_value=0.0, step=0.01)
    stock = st.number_input("Stock Quantity", min_value=0, step=1)
    submit_button = st.form_submit_button("Add Product to Database")

if submit_button:
    if name:
        payload = {"name": name, "price": price, "stock": stock}
        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 201:
                st.success(f"🎉 Successfully added '{name}' to the database!")
            else:
                error_details = response.json().get('detail', 'Unknown error')
                st.error(f"❌ Failed to add item: {error_details}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not reach backend server to send data.")
    else:
        st.warning("⚠️ Please provide a product name.")

st.markdown("---")

# --- SECTION 2: VIEW LIVE PRODUCTS ---
st.subheader("📦 Current Active Inventory")

try:
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        products = response.json()
        
        if not products:
            st.info("The database is currently empty. Add a product above!")
        else:
            for item in products:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                    with col1:
                        st.write(f"**ID:** {item['id']}")
                    with col2:
                        st.write(f"**Item:** {item['name']}")
                    with col3:
                        st.write(f"**Price:** ₹{item['price']:.2f}")
                    with col4:
                        st.write(f"**Stock:** {item['stock']} units")
                    st.markdown("")
except requests.exceptions.ConnectionError:
    st.error("❌ Could not connect to the backend server. Make sure your FastAPI app is running!")