# Setup
Put your **Pinecone API key**, your **Pincone index name**, and your **OpenAIAPI key** in the marked area in **main.py**

The app is based on **text-embedding-ada-002**

Use command **python -m streamlit run .\main.py** to run the app

# Usage
The app can search the content stored in vector database which has the closest meaning to your input content. It can be used to search paper content.

You can control Add to database or Search in Databse using natural language. If the app is unable to catch your opinion to add or search, it will tell you in the chat.
LLM in this app does not have memory . It only process your natural language input to categorize them into add or match behavior.
