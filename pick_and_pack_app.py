
import streamlit as st
import pandas as pd
import io

# Function to calculate the price based on the number of items
def calculate_price(num_items):
    if num_items <= 3:
        return 75 * 1.45  # Small tier with 45% margin
    elif 4 <= num_items <= 7:
        return 150 * 1.45  # Medium tier with 45% margin
    else:
        return (225 + (num_items - 7) * 25) * 1.45  # Large tier with 45% margin

# Function to calculate the total cost with margin
def calculate_total_cost(base_delivery_cost, duties_taxes, margin=0.45):
    return base_delivery_cost * (1 + margin) + duties_taxes * (1 + margin)

# Streamlit app
st.title("Pick and Pack Price Calculator")

# Input fields
num_items = st.number_input("Number of items", min_value=1, value=1)
base_delivery_cost = st.number_input("Base delivery cost (£)", min_value=0.0, value=0.0)
duties_taxes = st.number_input("Duties & taxes (£)", min_value=0.0, value=0.0)
payment_method = st.selectbox("Payment method", ["PO", "Card", "Retainer"])

# Calculate prices
pick_pack_price = calculate_price(num_items)
total_cost = calculate_total_cost(base_delivery_cost, duties_taxes) + pick_pack_price

# Display summary
st.subheader("Summary")
st.write(f"Pick and Pack Price (including 45% margin): £{pick_pack_price:.2f}")
st.write(f"Total Cost (including 45% margin): £{total_cost:.2f}")
st.write(f"Payment Method: {payment_method}")

# Create a DataFrame for the quote
quote_data = {
    "Description": [
        "Pick and Pack Price (including 45% margin)",
        "Base Delivery Cost",
        "Duties & Taxes",
        "Total Cost (including 45% margin)"
    ],
    "Amount (£)": [
        pick_pack_price,
        base_delivery_cost,
        duties_taxes,
        total_cost
    ]
}
quote_df = pd.DataFrame(quote_data)

# Download quote as Excel file
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Quote")
    processed_data = output.getvalue()
    return processed_data

excel_file = to_excel(quote_df)

st.download_button(
    label="Download Quote as Excel",
    data=excel_file,
    file_name="Pick_and_Pack_Quote.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
