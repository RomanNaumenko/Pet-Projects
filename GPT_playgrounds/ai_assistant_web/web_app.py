from datetime import datetime
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain import LLMChain
import pprint
import chromadb
from apikey import apikey
from langchain.vectorstores import Chroma
import os

os.environ["OPENAI_API_KEY"] = apikey
history = ChatMessageHistory()


def create_and_get_db():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma("langchain_store", embeddings, persist_directory='db')
    vectorstore.persist()
    retriever = vectorstore.as_retriever(search_kwargs=dict(k=2), search_type='mmr')
    memory = VectorStoreRetrieverMemory(retriever=retriever)
    memory.save_context({"input": "My favorite food is pizza"}, {"output": "thats good to know"})

    return memory, vectorstore


def get_chat_chain():
    _TEMPLATE = open('template.txt', 'r').read()
    PROMPT = PromptTemplate(
        input_variables=["history", "input"], template=_TEMPLATE
    )

    memory, _ = create_and_get_db()

    return ConversationChain(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2),
        prompt=PROMPT,
        memory=memory,
        verbose=True
    )


st.set_page_config(page_title='AI Assistant', page_icon='🦜')
st.title('🦜Your personal :blue[AI Assistant]🔗')
input_title = st.text_input('Please enter your message')

# Перевірка наявності введення в поле вводу
if input_title:
    # Прогнозування відповіді від AI та відображення її у вікні
    db_memory, db_vectorstore = create_and_get_db()
    output = get_chat_chain().predict(input=input_title)
    st.write(output)

    # Збереження повідомлень у ChatMessageHistory та збереження векторного простору
    history.add_user_message(input_title)
    history.add_ai_message(output)
    db_memory.save_context({"history": history}, {"output": output})
    db_vectorstore.persist()

    # Виведення історії повідомлень
    st.write('Conversation info:')
    st.info(messages_to_dict(history.messages), icon='🚨')
    pprint.pprint(messages_to_dict(history.messages))
