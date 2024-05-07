import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from apyori import apriori
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import openai  # Import the OpenAI library
import os
os.environ["sk-proj-BZH2oNyZt45UtGptMZ7iT3BlbkFJ37YZVGxkOyA948fihOtw"] = "sk-proj-BZH2oNyZt45UtGptMZ7iT3BlbkFJ37YZVGxkOyA948fihOtw"
# Set up OpenAI API key
openai.api_key = "sk-proj-BZH2oNyZt45UtGptMZ7iT3BlbkFJ37YZVGxkOyA948fihOtw"

# Define a function to generate a response from the OpenAI API
def get_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

st.set_option('deprecation.showPyplotGlobalUse', False)
file_bytes = st.file_uploader("Upload a file", type="csv")
words = st.sidebar.selectbox("No.of Words", range(10,1000,10))
st.image('smart.jpg', caption='Market Basket Analysis', use_column_width=True)

if file_bytes is not None:
    dataset = pd.read_csv(file_bytes, header=None)
    dim = dataset.shape
    rows = dim[0]
    cols = dim[1]
    print(rows, cols)
    transactions = []
    for i in range(0, rows):
        transactions.append([str(dataset.values[i,j]) for j in range(0, cols)])

    rule_list = apriori(transactions, min_support=0.003, min_confidence=0.1, min_lift=3, min_length=2)
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

# Add a section for the AI chat assistant
st.title('GroceryGenius Smart Grocery Shopping Using Basket Analysis')
st.header("AI Chat Assistant")
st.write("Ask me anything related to grocery shopping or basket analysis!")

# Create a text input for the user's question
user_input = st.text_area("Enter your question:")

# Create a button to submit the question
if st.button("Submit"):
    # Get the response from the OpenAI API
    response = get_response(user_input)

    # Display the response
    st.write(response)
