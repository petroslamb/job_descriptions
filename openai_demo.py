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

st.markdown("# A Job Description Demo 🎈")

st.markdown("### The Company :office:")
company = st.text_input("Company: ", value="Workable")
company_description = st.text_area(
    "Edit Company description: ", 
    value=call_the_model(
        f"Generate a short company description for {company}, to be used in the Job description later:"
        ).lstrip(),
)

st.markdown("### The Team :family:")
team = st.text_input("Team: ", value="Data Science")
team_description = st.text_area(
    "Edit Team description: ", 
    value=call_the_model(
        f"Generate a short team description for {team} at {company} with {company_description}, to be used in the Job description later:"
    ).lstrip(),
)

st.markdown("### The Role :camera:")
role = st.text_input("Role: ", value="Python Software Engineer")
role_description = st.text_area("Edit Role description: ", value=call_the_model(
    f"Generate a short role description for a {role} in {team} team ({team_description}), at company {company} ({company_description}), to be used in the Job description later:"
    ).lstrip()
)


st.markdown("### The skills :muscle:")
skills =st.text_area(
    "Edit Skills: ", 
    value=call_the_model(
        f"Generate a list of skills for a {role} ({role_description}) in {team} team ({team_description}), at company {company} ({company_description}), to be used in the Job description later:"
    ).lstrip(),
    height=200
)

skills_keywords = st.text_area(
    "Derived keywords:",
    call_the_model(
    f"Generate a list of comma separated keywords from the skills ({skills}):"
    ).lstrip()
)


st.markdown("### The Requirements :clipboard:")
requirements = st.text_area(
    "Edit Requirements: ",
    call_the_model(
        f"Generate a list of comma separated requirements for a {role} ({role_description}) in {team} team ({team_description}), at company {company} ({company_description}), with skills ({skills}) to be used in the Job description later:"
        ).lstrip(),
    height=200
    )
requirement_keywords = st.text_area(
    "Derived keywords:",
    call_the_model(
        f"Generate a list of comma separated keywords from the requirements ({requirements}): "
        ).lstrip()
    )


st.markdown("### The Sections :bookmark_tabs:")
sections = st.text_input(
    "Edit the Sections: ", 
    value="Introduction, Team, Role, Responsibilities, Requirements, Benefits"
    )


st.markdown("## The Job Description :memo:")
prompt = st.text_area(
    "Modify the prompt further to your liking: ", 
    value=(
        f"a job description for a {role}, in a {team} team, for the company {company}. " 
        )
    )

prompt_enriched = (
    f"{company_description}\n\n" +
    f"{team_description}\n\n" +
    f"{role_description}\n\n" +
    f"{skills_keywords}\n\n" +
    f"{requirement_keywords}\n\n" +
    f"Using the above, generate in Markdown {prompt}. The sections are: {sections}."
)

job_description = call_the_model(prompt_enriched)

st.markdown(job_description)

st.markdown("## The Interview Questions :question:")

open_ended_question = st.text_input(
    "Enter an open ended question here", 
    value="What is a list of technical interview questions, that relate to the job requirements?"
    )

st.write(call_the_model(job_description + "\n\n Q: " + open_ended_question + "\nA:"))
