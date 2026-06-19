# 🛒 E-Commerce Inventory Dashboard

A simple web application to manage product inventory. You can add items with prices in Rupees (₹), view your active stock, and delete items from a list.

## 🛠️ How it Works
* **The Webpage (`app.py`):** The visual dashboard with forms and buttons where you manage your items.
* **The Server (`main.py`):** The brain that checks your inputs (like making sure prices aren't negative) and passes data along.
* **The Database (`ecommerce.db`):** The storage file that saves your products permanently so they don't disappear when you close the app.

## 🚀 How to Run It

### Step 1: Install the requirements
Run this command in your terminal to install everything needed:
```bash
pip install fastapi uvicorn sqlalchemy pydantic streamlit requests
