import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 🎨 Themed UI Styling
st.markdown(
    """
    <style>
    body {background-color: #f8f6;}
    .big-font {font-size: 28px !important; font-weight: bold; color: #2c3e50;}
    .highlight {color: #ff6347; font-weight: bold;}
    .stButton>button {background: linear-gradient(to right, #007bff, #00c6ff); color: white; border-radius: 10px; padding: 10px;}
    .stProgress .bar {background-color: #4caf50 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 🎯 App Title & Description
st.title("💰 Smart Budget Analyzer")
st.subheader("📊 Track spending, analyze savings, and optimize your budget!")
st.write("---")

# 📊 Expense Categories
categories = ["Food", "Rent", "Entertainment", "Transportation", "Shopping", "Savings", "Other"]
budget = st.number_input("💵 Enter Your Monthly Budget ($)", min_value=100, step=50)

# 🔄 Dynamic Expense Input
expenses = {}
st.subheader("✏️ Enter Your Expenses in Each Category:")
for category in categories:
    expenses[category] = st.number_input(f"{category} ($)", min_value=0, step=10)

# 💡 Calculate Total Expenses & Savings
total_expenses = sum(expenses.values())
remaining_budget = budget - total_expenses
savings_percentage = (remaining_budget / budget) * 100 if budget > 0 else 0

# 📈 Display Results with Smooth Transition
if st.button("🚀 Analyze Budget"):
    with st.spinner("Analyzing your budget..."):
        time.sleep(2)  # Simulate loading
    
    summary_placeholder = st.empty()
    
    with summary_placeholder.container():
        st.markdown("<p class='big-font'>📊 Budget Summary:</p>", unsafe_allow_html=True)
        
        # 🚦 Budget Score with Progress Bar
        st.progress(int(savings_percentage))
        if savings_percentage > 20:
            st.success(f"✅ Excellent! 🎉 You're saving {savings_percentage:.1f}% of your income! 💰")
            st.snow()  # 🎊 Cool snow animation
        elif 10 <= savings_percentage <= 20:
            st.warning(f"⚠️ You're saving {savings_percentage:.1f}%. Try to increase savings!")
        else:
            st.error(f"❌ Low savings ({savings_percentage:.1f}%). Consider reducing expenses!")
            st.toast("Alert: Expenses exceeding limit! ⚠️")  # New toast notification
        
        # 📊 Interactive Bar Chart for Expenses
        df = pd.DataFrame({"Category": expenses.keys(), "Amount": expenses.values()})
        fig_bar = px.bar(df, x="Amount", y="Category", orientation='h', title="📊 Expense Breakdown", color="Amount", color_continuous_scale='blues')
        st.plotly_chart(fig_bar)
        
        # 🥧 Interactive Pie Chart for Spending Distribution
        fig_pie = px.pie(df, values='Amount', names='Category', title="💸 Spending Distribution", color_discrete_sequence=px.colors.sequential.RdBu, hole=0.3)
        st.plotly_chart(fig_pie)
        
        # 🔍 Budget Insights
        st.subheader("💡 Budget Insights:")
        if expenses["Entertainment"] > 0.2 * budget:
            st.warning("🎭 Reduce entertainment expenses to save more!")
        if expenses["Shopping"] > 0.2 * budget:
            st.warning("🛍️ Cut down on shopping for better budgeting!")

        st.info(f"📉 **Total Expenses:** ${total_expenses} | 📈 **Remaining Budget:** ${remaining_budget}")
        
        if savings_percentage > 10:
            st.balloons()  # 🎈 Celebration effect when savings are reasonable
