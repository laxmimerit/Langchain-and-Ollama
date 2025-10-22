# Youtube Streamlit Playlist
# https://www.youtube.com/watch?v=hff2tHUzxJM&list=PLc2rvfiptPSSpZ99EnJbH5LjTJ_nOoSWW

import streamlit as st

from dotenv import load_dotenv # langfuse or opik
from langchain_ollama import ChatOllama

from langchain_core.prompts import (
                                        SystemMessagePromptTemplate,
                                        HumanMessagePromptTemplate,
                                        ChatPromptTemplate,
                                        MessagesPlaceholder
                                        )


from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

from langchain_core.output_parsers import StrOutputParser

load_dotenv('./../.env')

st.title("Make Your Own Chatbot")
st.write("Chat with me! Catch me at https://youtube.com/kgptalkie")

base_url = "http://localhost:11434"
model = 'qwen3'

user_id = st.text_input("Enter your user id", "laxmikant")

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, connection = "sqlite:///chat_history.db")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Start New Conversation"):
    st.session_state.chat_history = []
    history = get_session_history(user_id)
    history.clear()


for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


### LLM Setup
llm = ChatOllama(base_url=base_url, model=model)

system = SystemMessagePromptTemplate.from_template("You are helpful assistant.")
human = HumanMessagePromptTemplate.from_template("{input}")

messages = [system, MessagesPlaceholder(variable_name='history'), human]

prompt = ChatPromptTemplate(messages=messages)

chain = prompt | llm | StrOutputParser()


runnable_with_history = RunnableWithMessageHistory(chain, get_session_history, 
                                                   input_messages_key='input', 
                                                   history_messages_key='history')

def chat_with_llm(session_id, input):
    for output in runnable_with_history.stream({'input': input}, config={'configurable': {'session_id': session_id}}):

        yield output


prompt = st.chat_input("What is up?")
# st.write(prompt)

if prompt:
    st.session_state.chat_history.append({'role': 'user', 'content': prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(chat_with_llm(user_id, prompt))

    st.session_state.chat_history.append({'role': 'assistant', 'content': response})