from datetime import datetime
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain import LLMChain
import pprint
import faiss
import chromadb
from apikey import apikey
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS, Chroma
import os

os.environ["OPENAI_API_KEY"] = apikey


def create_and_get_db():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma("langchain_store", embeddings, persist_directory='.')
    if not (os.path.exists('chroma-collections.parquet') and os.path.exists('chroma-embeddings.parquet')):
        vectorstore.persist()
    retriever = vectorstore.as_retriever(search_kwargs=dict(k=4), search_type='mmr')
    memory = VectorStoreRetrieverMemory(retriever=retriever)
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


while True:
    human_input = input("Human:")
    output = get_chat_chain().predict(input=human_input)
    pprint.pprint(output)
    db_memory, db_vectorstore = create_and_get_db()
    db_memory.save_context({"input": human_input}, {"output": output})
    db_vectorstore.persist()


# st.title = '🦜AI Assistant🔗'