from datetime import datetime
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

import faiss
import chromadb

from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS, Chroma
import os
os.environ["OPENAI_API_KEY"] = "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"


# embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
# index = faiss.IndexFlatL2(embedding_size)
# embedding_fn = OpenAIEmbeddings().embed_query
# vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})
embeddings = OpenAIEmbeddings()
vectorstore = Chroma("langchain_store", embeddings, persist_directory='.')
vectorstore.persist()

# In actual usage, you would set `k` to be a higher value, but we use k=1 to show that
# the vector lookup still returns the semantically relevant information
retriever = vectorstore.as_retriever(search_kwargs=dict(k=1))
memory = VectorStoreRetrieverMemory(retriever=retriever)

# When added to an agent, the memory object can save pertinent information from conversations or used tools
memory.save_context({"input": "My favorite food is pizza"}, {"output": "thats good to know"})
memory.save_context({"input": "My favorite sport is soccer"}, {"output": "..."})
memory.save_context({"input": "I don't the Celtics"}, {"output": "ok"}) #
# Notice the first result returned is the memory pertaining to tax help, which the language model
# deems more semantically relevant
# to a 1099 than the other documents, despite them both containing numbers.
# print(memory.load_memory_variables({"prompt": "what sport should i watch?"})["history"])

llm = OpenAI(temperature=0) # Can be any valid LLM
_DEFAULT_TEMPLATE = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions 
to providing in-depth explanations and discussions on a wide range of topics. As a language model, 
Assistant is able to generate human-like text based on the input it receives, allowing it to engage 
in natural-sounding conversations and provide responses that are coherent and relevant to the topic 
at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able 
to process and understand large amounts of text, and can use this knowledge to provide accurate and 
informative responses to a wide range of questions. Additionally, Assistant is able to generate its 
own text based on the input it receives, allowing it to engage in discussions and provide explanations 
and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable 
insights and information on a wide range of topics. Whether you need help with a specific question or 
just want to have a conversation about a particular topic, Assistant is here to assist.

Relevant pieces of previous conversation:
{history}
(You need to always use previous pieces of conversations)

Current conversation:
Human: {input}
Assistant:"""

PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=_DEFAULT_TEMPLATE
)
conversation_with_summary = ConversationChain(
    llm=llm,
    prompt=PROMPT,
    # We set a very low max_token_limit for the purposes of testing.
    memory=memory,

)
while True:
    human_input = input("Human:")
    output = conversation_with_summary.predict(input=human_input)
    print(output)
    memory.save_context({"input": human_input}, {"output": output})