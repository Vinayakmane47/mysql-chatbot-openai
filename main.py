import streamlit as st
from openai import OpenAI
from langchain_community.utilities.sql_database import SQLDatabase

from src.sql_generator import invoke_chain
#from langchain_utils import invoke_chain
from langchain_core.messages import AIMessage , HumanMessage

st.title("MySQL Database Chatbot")

def init_database(user:str,password:str,host:str,port:str,database:str): 
    db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

if "chat_history" not in st.session_state: 
    st.session_state.chat_history = [
        AIMessage("Hello! I'm a SQL assistant . Ask me anything about your mysql database."),
        HumanMessage("hi")
    ]


with st.sidebar: 
    st.subheader("Settings") 
    st.write("This is simple chat application using MySQL . Connect to database ")

    st.text_input("Host",value="localhost",key="Host")
    st.text_input("Port",value="3306",key="Port")
    st.text_input("User",value="root",key="User")
    st.text_input("Password",type="password", value="sak$103138",key="Password")
    st.text_input("Database",value="classicmodels",key="Database")

    if st.button("Connect"): 
        with st.spinner("Connecting to Database...."): 
            db = init_database(
            st.session_state["User"],
            st.session_state['Password'] ,
            st.session_state['Host'],
            st.session_state['Port'],
            st.session_state['Database']
            ) 
            st.session_state.db = db 
            st.success("Connected to database!")


for message in st.session_state.chat_history: 
    if isinstance(message,AIMessage): 
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message,HumanMessage): 
        with st.chat_message("Human"): 
            st.markdown(message.content)

# Set OpenAI API key from Streamlit secrets
#client = OpenAI(api_key="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")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    # print("Creating session state")
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            response = invoke_chain(st.session_state.db ,prompt,st.session_state.messages)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})