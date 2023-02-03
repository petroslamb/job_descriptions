import os
import streamlit as st
import openai

st.sidebar.markdown("# OpenAI Demo 🎈")

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

model_list = openai.Model.list()
model_names = [model["id"] for model in model_list["data"]]


model_names = ["text-davinci-003"] + model_names

model = st.sidebar.selectbox("Select a model", model_names, index=0)

# Get the model for the selected model
st.sidebar.write(openai.Model.retrieve(model))


@st.cache
def call_the_model(prompt, max_tokens=550):
    result = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=0.9,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return result['choices'][0]['text']

st.markdown("# Job Description Demos 🎈")

