import sys  
import streamlit as st
import pandas as pd 
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

dataset = pd.read_csv('Market.csv', header=None)
dataset.dropna(how='all', inplace=True)  
transactions = dataset.apply(lambda x: x.dropna().tolist(), axis=1).tolist()
transactions = [[item.lower() for item in transaction] for transaction in transactions]
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)
frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

def recommend_products(basket, rules):
    basket_set = set(basket)  
    recommendations = set()

    for product in basket_set:
        product_rules = rules[rules['antecedents'].apply(lambda x: product in set(x))]
        for _, row in product_rules.iterrows():
            recommendations.update([item for item in row['consequents'] if item not in basket_set])

    return sorted(recommendations)

def run_app():
    st.markdown(
        """
        <style>
        body {
            background-image: url('smart.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .container {
            padding: 10px;
            background-color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Smart Grocery Shopping Assistant with Basket Analysis App")
    st.image("smart.jpg", use_column_width=True)

    with st.container():
        unique_items = sorted(set(item for sublist in transactions for item in sublist))
        selected_item = st.selectbox("Select an item to add to your cart", unique_items)

        if 'cart_items' not in st.session_state:
            st.session_state.cart_items = []

        if st.button('Add to Cart'):
            st.session_state.cart_items.append(selected_item.lower())
            st.session_state.cart_items = list(set(st.session_state.cart_items))

        st.write("Your Cart:", ", ".join(st.session_state.cart_items))

        if st.session_state.cart_items:
            recommendations = recommend_products(st.session_state.cart_items, rules)
            if recommendations:
                st.write("Recommendations for you:", ", ".join(recommendations))
            else:
                st.write("No recommendations available.")

if __name__ == "__main__":
    run_app()
       