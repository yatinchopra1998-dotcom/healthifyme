import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


# Use a proper env var name and check it
gemini_api_key = os.getenv('test-project-1')

if not gemini_api_key:
    st.error("GEMINI_API_KEY not set. Set the environment variable and restart the app.")
else:
    model = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash-lite',
        api_key=gemini_api_key,
        temperature=0.7,
    )

st.title(':orange[HealthifyMe]: Your Personal Health Assistant')
st.markdown("""
            This application will assist you to get better and customized Health advice.
            You can ask questions related to fitness, nutrition, and overall well-being.
            """)

# Lets design the sidebar for user parameters
st.sidebar.header(':red[Enter Your Details Here:]')
name = st.sidebar.text_input('Name')
age = st.sidebar.text_input('Age')
gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
height = st.sidebar.text_input('Height (cm)')
weight = st.sidebar.text_input('Weight (kg)')
bmi = pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)
activity_level = st.sidebar.slider('Rate your Activity Level',0,5,step=1)
fitness = st.sidebar.slider('Rate your Fitness Level',0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f'{name} ,your BMI is: {bmi:.2f}kg/m²')

# Lets use the Gemini model to generate the report based on user input
user_input = st.text_input('Ask your Health related questions here:')

prompt =f'''
<role> You are an expert Health and Fitness Advisor and has 10+ years of experience in health related
guidance. Provide personalized advice based on the user's details and questions. </role>
<goal> Generate the customized health advice report based on user input, addressing the problem the user has asked.
Here is the question that user has asked: {user_input} </goal>
<context> Here are the details that user has provided:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi:.2f} kg/m²
- Activity Level(0-5): {activity_level}
- Fitness Level(0-5): {fitness}
</context>
<format> Start with the greeting using user's name, then provide a detailed and structured health advice report by first identifying the problem,
identifying the root cause of the problem and remedies. Mention the doctor from which specialization can be visited if required.
Mention any change in the diet plan which is required. Use bullet points or numbered lists where appropriate for clarity.
Go step by step so that it is completely clear. In last create a final summary of all the things that has been discussed.
Conclude with motivational tips to encourage a healthy lifestyle. 
</format>
<Instructions> Strictly do not advice any medicines. If the problem seems serious, always recommend consulting a healthcare professional for accurate diagnosis and treatment.</format>

'''

if st.button('Get Health Advice'):
    print(user_input)
    print('\n')
    print('Generating...')
    response = model.invoke(prompt)
    st.write(response.content)