import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from apyori import apriori
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import requests
#


import openai

# Set up OpenAI API
openai.api_key = "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"

# Function to interact with OpenAI API
# Function to interact with OpenAI API
def ask_ai(question):
    response = openai.Completion.create(
        engine="davinci",  # You can choose different models like davinci-codex, davinci-instruct-beta, etc.
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Main Streamlit app code
st.title("AI Assistant for General Questions")

question = st.text_input("Ask your question here:")
if question:
    answer = ask_ai(question)
    st.write("AI's Response:")
    st.write(answer)


#


st.title('GroceryGenius Smart Grocery Shopping Using Basket Analysis')

st.set_option('deprecation.showPyplotGlobalUse', False)
file_bytes = st.file_uploader("Upload a file", type="csv")
words = st.sidebar.selectbox("No.of Words", range(10,1000,10))

st.image('smart.jpg', caption='Market Basket Analysis', use_column_width=True)

if file_bytes is not None:
    dataset = pd.read_csv(file_bytes, header = None)
    dim = dataset.shape
    rows = dim[0]
    cols = dim[1]
    print(rows, cols)
    transactions = []
    for i in range(0, rows):
        transactions.append([str(dataset.values[i,j]) for j in range(0, cols)])
    rule_list = apriori(transactions, min_support = 0.003, min_confidence = 0.1, min_lift = 3, min_length = 2)
    results = list(rule_list)
    bought_item = [tuple(result[2][0][0])[0] for result in results]
    will_buy_item = [tuple(result[2][0][1])[0] for result in results]
    support_values = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lift_values = [result[2][0][3] for result in results]
    new_data = list(zip(bought_item, will_buy_item, support_values, confidences, lift_values))
    new_df = pd.DataFrame(new_data, columns=["Bought Item", "Expected To Be Bought", "Support", "Confidence", "Lift"])

    st.sidebar.header("Select Item")
    Input = st.sidebar.selectbox('Object Variables', new_df["Bought Item"])
    print(Input)
    sample = new_df[new_df['Bought Item'] == Input]
    lis1 = []
    for i in sample["Expected To Be Bought"]:
        lis1.append(i)
    space = " "
    output = space.join(lis1)
    output_final = output.replace("nan", "")
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 32px;">Recommended Items for above selected Item</p>'
    st.markdown(new_title, unsafe_allow_html=True)

    st.write(output_final)
    st.write("Word Cloud Plot")
    wordcloud = WordCloud(background_color="white", max_words=words).generate(output_final)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()

# Add a button to recommend recipes
recommend_recipes_button = st.button("Recommend Recipes")

# Handle button click event
if recommend_recipes_button:
    st.session_state.selected_groceries = [Input]  # Store selected groceries in session state
    st.header("Recipe Recommendations")
    recipes = get_recipe_recommendations(st.session_state.selected_groceries)
    if recipes:
        for recipe in recipes:
            st.subheader(recipe['title'])
            st.write("Ingredients:", ", ".join(recipe['ingredients']))
            st.write("Instructions:", recipe['instructions'])
            st.write("Link:", recipe['url'])
    else:
        st.write("No recipe recommendations available.")
