import openai
import streamlit as st
import toml

secrets = toml.load("streamlit/secrets.toml")

st.title("Chat Bot (GPT-3.5)")

openai.api_key = secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        response = openai.Completion.create(
            engine=st.session_state["openai_model"],
            prompt="\n".join(m["content"] for m in st.session_state.messages),
            max_tokens=150
        )
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].text.strip()})

    with st.chat_message("assistant"):
        st.markdown(st.session_state.messages[-1]["content"])
