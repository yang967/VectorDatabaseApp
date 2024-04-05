# Setup
Put your Pinecone API key and your Pincone index name in the marked area in **main.py**

The app is based on **text-embedding-ada-002**

Use command **python -m streamlit run .\main.py** to run the app

# Usage
The app can search the content stored in vector database which has the closest meaning to your input content. It can be used to search paper based on pdf file.

You can put **[Add to Database]:** at the start of the prompt to add the content to the database. ex. Use *[Add to Database]: Hello World* to add *Hello World* to Database. **There has to be a space after ':'**
