import streamlit as st
from pinecone import Pinecone
import re
from openai import OpenAI

pc = Pinecone(api_key="Your Pinecone API key goes here")
index = pc.Index("Your Pinecone index name goes here")

StartPrompt = "You need to categorize the user input from natural language into 3 different types based on input content: Match, Add. Match category means user want to match the content with content in the database. Add means user want to add content to the database. Your output content should strictly in the following format Match/Add: Summarized Content that user want to match or add. You should not include extra words in summarized content."

client = OpenAI(api_key='Your OpenAI API key goes here')

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

def Processing(text):
    messages = [
        {"role": "system", "content": "You need to categorize the user input from natural language into 3 different types based on input content: Match, Add. Match category means user want to match the content with content in the database. Add means user want to add content to the database. Your output content should strictly in the following format Match/Add: Summarized Content that user want to match or add. You should not include extra words in summarized content."},
        {"role": "user", "content": text}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages, 
        temperature=2
    )

    returned_message = response.choices[0].message.content
    print(returned_message)
    if ": " not in returned_message:
        return returned_message
    
    separations = returned_message.split(": ")
    content = ""
    i = 1
    while i < len(separations):
        content += separations[i]
        i += 1

    if separations[0] == "Add" or separations[0] == 'add':
        AddToDatabase(content)
        return content + ' has been added to database'
    else:
        return QueryDatabase(content)

st.title("Content Searching Tool")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if prompt:= st.chat_input("Input text here"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content":prompt})


if prompt == None:
    response = prompt
else:
    response = Processing(prompt)

with st.chat_message("assistant"):
    st.markdown(response)
st.session_state.messages.append({"role": "assistant", "content": response})