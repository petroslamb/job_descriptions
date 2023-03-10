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

st.markdown("# A Job Description Demo 2")

st.markdown("## General info :memo:")
company = st.text_input("Company: ", value="Workable")
team = st.text_input("Team: ", value="Data Science")
role = st.text_input("Role: ", value="Python Software Engineer")

st.markdown("### Descriptions :pencil2:")

with st.expander("Edit descriptions"):
    company_description = st.text_area(
        "Edit Company description: ", 
        value=call_the_model(
            f"Generate a short company description for {company}, to be used in the Job description later:"
            ).lstrip(),
    )
    team_description = st.text_area(
        "Edit Team description: ", 
        value=call_the_model(
            f"Generate a short team description for {team} at {company} with {company_description}, to be used in the Job description later:"
        ).lstrip(),
    )
    role_description = st.text_area("Edit Role description: ", value=call_the_model(
        f"Generate a short role description for a {role} in {team} team ({team_description}), at company {company} ({company_description}), to be used in the Job description later:"
        ).lstrip()
    )


st.markdown("### Responsibilities and Requirements :clipboard:")

with st.expander("Edit responsibilities and requirements"):
    responsibilities =st.text_area(
        "Edit responsibilities: ", 
        value=call_the_model(
            f"Generate a list of comma separated keywords of responsibilities for a {role} ({role_description}) in {team} team ({team_description}), at company {company} ({company_description}), to be used in the Job description:"
        ).lstrip(),
        height=200
    )

    requirements = st.text_area(
        "Edit Requirements: ",
        call_the_model(
            f"Generate a list of education, technical and soft requirements for a {role} ({role_description}) in {team} team ({team_description}), at company {company} ({company_description}), with responsibilities ({responsibilities}) to be used in the Job description later:"
            ).lstrip(),
        height=200
        )


st.markdown("### The Job Description :memo:")

sections = st.text_input(
    "Edit the Sections: ", 
    value="Introduction, Team, Role, Responsibilities, Requirements, Benefits"
    )

job_button = st.button("Generate the job description")

if job_button:

    prompt = st.text_area(
        "Modify the prompt further to your liking: ", 
        value=(
            f"a job description for a {role}, in a {team} team, for the company {company}. " 
            )
        )

    prompt_enriched = (
        f"Company: {company}\n\n" +
        f"Company description: {company_description}\n\n" +
        f"Team: {team}\n\n" +
        f"Team description: {team_description}\n\n" +
        f"Role: {role}\n\n" +
        f"Role description: {role_description}\n\n" +
        f"Responsibilities keywords: {responsibilities}\n\n" +
        f"Job requirements: {requirements}\n\n" +
        f"Using the above provided information, generate in Markdown {prompt}. " + 
        f"Use the Responsibilities and requirements keywords to generate the relevant sections of the job description."
        f"The sections of the job description are: {sections}."
    )

    job_description = call_the_model(prompt_enriched, max_tokens=1000)

    st.markdown(job_description)

    st.markdown("### The Interview Questions :question:")


    with st.expander("Open the interview questions"):
        interview_question = st.text_input(
            "Edit the interview question:", 
            value="What is a list of technical interview questions, that relate to the job requirements?"
            )
        st.write(call_the_model(job_description + "\n\n Q: " + interview_question + "\nA:"))
