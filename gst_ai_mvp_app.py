import streamlit as st
import pandas as pd

# --- Safe sum function ---
def safe_sum(series):
    return pd.to_numeric(series, errors="coerce").fillna(0).sum()

# --- Smart column finder ---
def find_column(df, possible_names):
    """Find column by checking multiple possible names (case-insensitive)"""
    df_cols_lower = [col.lower().strip() for col in df.columns]
    
    for name in possible_names:
        name_lower = name.lower().strip()
        if name_lower in df_cols_lower:
            # Return the original column name
            index = df_cols_lower.index(name_lower)
            return df.columns[index]
    return None

# --- FLEXIBLE GSTR-3B summary generator ---
def generate_gstr3b_summary(sales_df, purchases_df):
    summary = {}
    
    st.write("### 🔍 SMART COLUMN DETECTION")
    
    # Possible column name variations
    taxable_names = ["TaxableValue", "Taxable_Value", "taxablevalue", "taxable value", "amount", "Amount", "value", "Value", "Taxable Amount", "taxable_amount"]
    cgst_names = ["CGST", "cgst", "CGST_Amount", "cgst_amount", "cgst amount", "Central GST", "central_gst"]
    sgst_names = ["SGST", "sgst", "SGST_Amount", "sgst_amount", "sgst amount", "State GST", "state_gst"]  
    igst_names = ["IGST", "igst", "IGST_Amount", "igst_amount", "igst amount", "Integrated GST", "integrated_gst"]
    
    # Find columns in sales data
    sales_taxable_col = find_column(sales_df, taxable_names)
    sales_cgst_col = find_column(sales_df, cgst_names)
    sales_sgst_col = find_column(sales_df, sgst_names)
    sales_igst_col = find_column(sales_df, igst_names)
    
    st.write("**SALES CSV - Column Mapping:**")
    st.write(f"- Taxable Value: {sales_taxable_col if sales_taxable_col else '❌ Not found'}")
    st.write(f"- CGST: {sales_cgst_col if sales_cgst_col else '❌ Not found'}")
    st.write(f"- SGST: {sales_sgst_col if sales_sgst_col else '❌ Not found'}")  
    st.write(f"- IGST: {sales_igst_col if sales_igst_col else '❌ Not found'}")
    
    # Find columns in purchases data
    purch_taxable_col = find_column(purchases_df, taxable_names)
    purch_cgst_col = find_column(purchases_df, cgst_names)
    purch_sgst_col = find_column(purchases_df, sgst_names)
    purch_igst_col = find_column(purchases_df, igst_names)
    
    st.write("**PURCHASES CSV - Column Mapping:**")
    st.write(f"- Taxable Value: {purch_taxable_col if purch_taxable_col else '❌ Not found'}")
    st.write(f"- CGST: {purch_cgst_col if purch_cgst_col else '❌ Not found'}")
    st.write(f"- SGST: {purch_sgst_col if purch_sgst_col else '❌ Not found'}")
    st.write(f"- IGST: {purch_igst_col if purch_igst_col else '❌ Not found'}")
    
    # If no columns found, let user manually select
    if not sales_taxable_col:
        st.error("🚨 **MANUAL COLUMN SELECTION NEEDED**")
        st.write("**Available Sales Columns:**", list(sales_df.columns))
        
        # Let user select columns manually
        sales_taxable_col = st.selectbox("Select SALES Taxable Value Column:", 
                                       ["None"] + list(sales_df.columns), key="sales_taxable")
        sales_cgst_col = st.selectbox("Select SALES CGST Column:", 
                                    ["None"] + list(sales_df.columns), key="sales_cgst")
        sales_sgst_col = st.selectbox("Select SALES SGST Column:", 
                                    ["None"] + list(sales_df.columns), key="sales_sgst")
        sales_igst_col = st.selectbox("Select SALES IGST Column:", 
                                    ["None"] + list(sales_df.columns), key="sales_igst")
        
        # Convert "None" to None
        sales_taxable_col = sales_taxable_col if sales_taxable_col != "None" else None
        sales_cgst_col = sales_cgst_col if sales_cgst_col != "None" else None
        sales_sgst_col = sales_sgst_col if sales_sgst_col != "None" else None
        sales_igst_col = sales_igst_col if sales_igst_col != "None" else None
    
    if not purch_taxable_col:
        st.write("**Available Purchase Columns:**", list(purchases_df.columns))
        
        # Let user select columns manually  
        purch_taxable_col = st.selectbox("Select PURCHASE Taxable Value Column:", 
                                       ["None"] + list(purchases_df.columns), key="purch_taxable")
        purch_cgst_col = st.selectbox("Select PURCHASE CGST Column:", 
                                    ["None"] + list(purchases_df.columns), key="purch_cgst")
        purch_sgst_col = st.selectbox("Select PURCHASE SGST Column:", 
                                    ["None"] + list(purchases_df.columns), key="purch_sgst")
        purch_igst_col = st.selectbox("Select PURCHASE IGST Column:", 
                                    ["None"] + list(purchases_df.columns), key="purch_igst")
        
        # Convert "None" to None
        purch_taxable_col = purch_taxable_col if purch_taxable_col != "None" else None
        purch_cgst_col = purch_cgst_col if purch_cgst_col != "None" else None
        purch_sgst_col = purch_sgst_col if purch_sgst_col != "None" else None
        purch_igst_col = purch_igst_col if purch_igst_col != "None" else None
    
    # Calculate summary using found/selected columns
    summary["Outward Taxable Value"] = safe_sum(sales_df[sales_taxable_col]) if sales_taxable_col else 0
    summary["Outward CGST"] = safe_sum(sales_df[sales_cgst_col]) if sales_cgst_col else 0
    summary["Outward SGST"] = safe_sum(sales_df[sales_sgst_col]) if sales_sgst_col else 0
    summary["Outward IGST"] = safe_sum(sales_df[sales_igst_col]) if sales_igst_col else 0
    
    summary["Inward Taxable Value"] = safe_sum(purchases_df[purch_taxable_col]) if purch_taxable_col else 0
    summary["Inward CGST"] = safe_sum(purchases_df[purch_cgst_col]) if purch_cgst_col else 0
    summary["Inward SGST"] = safe_sum(purchases_df[purch_sgst_col]) if purch_sgst_col else 0
    summary["Inward IGST"] = safe_sum(purchases_df[purch_igst_col]) if purch_igst_col else 0
    
    return summary

# --- Streamlit App ---
st.title("🚀 ULTIMATE FLEXIBLE GST AI Tool")
st.markdown("**Works with ANY CSV format!** Automatically detects column names or lets you select manually.")

uploaded_sales = st.file_uploader("📤 Upload Sales CSV", type=["csv"])
uploaded_purchases = st.file_uploader("📤 Upload Purchases CSV", type=["csv"])

if uploaded_sales and uploaded_purchases:
    try:
        # Try different separators and encodings
        sales_df = None
        purchases_df = None
        
        # Try comma separator first
        try:
            sales_df = pd.read_csv(uploaded_sales, sep=',')
            purchases_df = pd.read_csv(uploaded_purchases, sep=',')
        except:
            try:
                # Try semicolon separator
                sales_df = pd.read_csv(uploaded_sales, sep=';')
                purchases_df = pd.read_csv(uploaded_purchases, sep=';')
            except:
                # Try tab separator
                sales_df = pd.read_csv(uploaded_sales, sep='\t')
                purchases_df = pd.read_csv(uploaded_purchases, sep='\t')

        st.success("✅ CSV files loaded successfully!")
        
        # Show raw data
        with st.expander("📊 Raw Data Preview"):
            st.write("**Sales Data:**")
            st.dataframe(sales_df.head())
            st.write("**Available Sales Columns:**", list(sales_df.columns))
            
            st.write("**Purchase Data:**")  
            st.dataframe(purchases_df.head())
            st.write("**Available Purchase Columns:**", list(purchases_df.columns))

        # Generate summary with smart detection
        summary = generate_gstr3b_summary(sales_df, purchases_df)

        st.markdown("---")
        st.subheader("📋 GSTR-3B Summary")
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 OUTWARD SUPPLIES")
            st.metric("Taxable Value", f"₹{summary['Outward Taxable Value']:,.2f}")
            st.metric("CGST", f"₹{summary['Outward CGST']:,.2f}")
            st.metric("SGST", f"₹{summary['Outward SGST']:,.2f}")
            st.metric("IGST", f"₹{summary['Outward IGST']:,.2f}")
        
        with col2:
            st.markdown("### 📉 INWARD SUPPLIES")
            st.metric("Taxable Value", f"₹{summary['Inward Taxable Value']:,.2f}")
            st.metric("CGST", f"₹{summary['Inward CGST']:,.2f}")
            st.metric("SGST", f"₹{summary['Inward SGST']:,.2f}")
            st.metric("IGST", f"₹{summary['Inward IGST']:,.2f}")

        # Final calculation
        gst_payable = summary["Outward CGST"] + summary["Outward SGST"] + summary["Outward IGST"]
        gst_credit = summary["Inward CGST"] + summary["Inward SGST"] + summary["Inward IGST"]
        net_gst = gst_payable - gst_credit

        st.markdown("---")
        st.subheader("💰 FINAL CALCULATION")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💳 Total GST Payable", f"₹{gst_payable:,.2f}")
        with col2:
            st.metric("💰 Input Tax Credit", f"₹{gst_credit:,.2f}")
        with col3:
            if net_gst > 0:
                st.metric("⚠️ Net GST Liability", f"₹{net_gst:,.2f}")
            elif net_gst < 0:
                st.metric("✅ GST Refund Due", f"₹{abs(net_gst):,.2f}")
            else:
                st.metric("✅ No GST Payable", "₹0.00")

    except Exception as e:
        st.error(f"❌ Error loading CSV: {str(e)}")
        st.write("**Try these troubleshooting steps:**")
        st.write("1. Make sure your CSV file is properly formatted")
        st.write("2. Check if you're using semicolon (;) instead of comma (,) as separator")
        st.write("3. Ensure no special characters in column names")

else:
    st.info("👆 Upload both CSV files to start automatic detection!")
    st.write("**This tool will:**")
    st.write("✅ Auto-detect column names")
    st.write("✅ Handle different CSV formats (comma, semicolon, tab)")
    st.write("✅ Let you manually select columns if needed")
    st.write("✅ Work with ANY column naming convention!")