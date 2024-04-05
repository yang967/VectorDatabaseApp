import streamlit as st
from pinecone import Pinecone
import re
from openai import OpenAI

pc = Pinecone(api_key="Your Pinecone API key goes here")
index = pc.Index("Your Pinecone Index Name goes here")

client = OpenAI()

def get_embedding(text):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model = "text-embedding-ada-002").data[0].embedding

def AddToDatabase(text):
    embedding = get_embedding(text)
    index.upsert([{"id": text, "values": embedding}])

def QueryDatabase(text):
    embedding = get_embedding(text)
    result = index.query(
        vector=embedding,
        top_k=1,
        include_values=False,
        include_metadata=False
    )
    return result['matches'][0]['id']

st.title("Content Searching Tool")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if prompt:= st.chat_input("Input text here"):
    if re.search("^\[Add to Database\]: ", prompt):
        print("add")
    with st.chat_message("user"):
        st.markdown(prompt)
    txt = prompt
    if re.search("^\[Add to Database\]: ", prompt):
        txt = re.sub('^\[Add to Database\]: ', '', txt)
        AddToDatabase(txt)
    st.session_state.messages.append({"role": "user", "content":prompt})


if prompt == None:
    response = prompt
else:    
    if not re.search("^\[Add to Database\]: ", prompt):
        response = QueryDatabase(prompt)
    else:
        prompt = re.sub('^\[Add to Database\]: ', '', prompt)
        response = prompt + ' has been added to database'

with st.chat_message("assistant"):
    st.markdown(response)
st.session_state.messages.append({"role": "assistant", "content": response})