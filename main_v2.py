import toml
import streamlit as st
from streamlit_chat import message
import random
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from src.scrapper import ScrapeWebPage
from src.compressed_search import SimilarityCalculator
from src.vector_search import VectorSearch
from src.get_response import ResponseLLM
from src.ollama import OllamaGeneration

if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.contect= []

st.set_page_config(page_title="Suave AI", page_icon="🌐")
with st.sidebar:
    st.title('🦙💬 Suave AI')
    st.write('Suave AI is a pioneering company specializing in the development of cutting-edge chatbot \
        solutions tailored for businesses across various industries. Leveraging advanced artificial intelligence \
            technology, Suave AI empowers organizations to enhance customer engagement, streamline operations, \
                and drive growth through intuitive and intelligent chatbot interactions. ')

    url = st.text_input("Please add a URL: ")
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    # top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)
    st.markdown('📖 Check out our webpage [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

  

@st.cache_data()
def scrape_url(url):
    url_scrapper = ScrapeWebPage(url)
    url_list, base_url = url_scrapper.get_url()
    processed_url = url_scrapper.process_urls(url_list=url_list, base_url=base_url)
    content = url_scrapper.get_page_contents_markdown(url_list = set(processed_url))
    print(content)
    vector_obj = VectorSearch(data=content, model_name="sentence-transformers/msmarco-distilbert-base-v3")
    # vector_obj = VectorSearch(data=content, model_name="BAAI/bge-small-en-v1.5")
    return vector_obj

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("`Ask a question:`")

if url:
    with st.spinner("Scraping the webpage. Please wait."):
        vector_obj=scrape_url(url=url)


if query:
    with st.chat_message("user"):
        st.write(query)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            docs, metadatas = vector_obj._split_data_markdown()
            data_store = vector_obj._faiss_search()
            result = data_store.similarity_search(query)
            context = result[0].page_content
            answer_response = ResponseLLM(
                context=context,
                question=query,   
            ).generate_markdown()
            st.session_state.messages.append({"role": "user", "content": query, "context": context})
            st.markdown(answer_response)
            st.write(result[0].metadata["source"])
            st.session_state.messages.append({"role": "assistant", "content": answer_response, "context": context})

