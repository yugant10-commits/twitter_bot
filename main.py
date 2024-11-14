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
from PIL import Image

if 'messages' not in st.session_state:
    opener = 'こんにちは！Xのことなら何でも聞いてください（旧ツイッター）'
    print('problem remover here')
    st.session_state.messages = [{"role": "assistant", "content": opener}]
    print(f'problem remover here{st.session_state.messages}')
    st.session_state.content= []
    st.session_state.context = []

im = Image.open("./images/favicon.png")
st.set_page_config(page_title="x-chatbot.ai", page_icon=im)

with st.sidebar:
    st.image('images/x-logo.png')
    new_title = '<p style="font-family: sans-serif; color:Black; font-size: 16px;">From <b>questions</b> to <b>instant answers.</b></p>'
    url_page = '<b style="font-family: sans-serif; color:Black; font-size: 12px;"></b>'
    st.markdown(new_title, unsafe_allow_html=True)
    st.markdown("##")
    st.markdown("##")
    st.markdown(url_page, unsafe_allow_html=True)
    new_title = '<p style="font-family: sans-serif; color:Black; font-size: 16px;">このボットはX（旧Twitter）のFAQの質問のほとんどを把握しています。Xに関することなら何でも質問できます。</p>'
    url_page = '<b style="font-family: sans-serif; color:Black; font-size: 12px;"></b>'
    st.markdown(new_title, unsafe_allow_html=True)
    # url = st.text_input("Please add a URL below to scrape your knowledge base.")
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    
    footer_info = '''<span style="font-family: Fantasy; color: black; font-size: 13px">
    We have all the pricing and information mentioned in our webpage.
    📖 Keep Waiting.'''
    new_title = '<p style="font-family: sans-serif; color:Black; font-size: 16px;">Developed by: </p>'
    url_page = '<b style="font-family: sans-serif; color:Black; font-size: 12px;"></b>'
    st.markdown(new_title, unsafe_allow_html=True)
    st.image('images/tai.png')
    st.markdown(footer_info, unsafe_allow_html=True)

def file_to_list(file_path:str)->list:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    texts = [line.strip() for line in lines]
    return texts
import time

@st.cache_resource()
def scrape_url(url):
    url_scrapper = ScrapeWebPage(url)
    # url_list, base_url = url_scrapper.get_url()
    # processed_url = url_scrapper.process_urls(url_list=url_list, base_url=base_url)
    links = file_to_list(file_path="./raw-links.txt")
    content = url_scrapper.get_page_contents(url_list = set(links))
    vector_obj = VectorSearch(data=content, model_name="text-embedding-3-large")
    start_time = time.time()
    docs, metadatas = vector_obj._split_data()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Split data time: {elapsed_time}")
    start_time = time.time()
    data_store = vector_obj._faiss_search()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"vector store creation: {elapsed_time}")
    return data_store

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
query = st.chat_input("Please add your query")

# if url:
#     with st.spinner("Scraping the webpage. Please wait."):

data_store=scrape_url(url="https://help.x.com/en/using-x")


if query:
    with st.chat_message("user"):
        st.write(query)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()
            result = data_store.similarity_search(query)
            context = result[0].page_content
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"Similarity searchtime : {elapsed_time}")

            start_time = time.time()
            answer_response = ResponseLLM(
                context=context,
                question=query,   
            )._generate()
            end_time = time.time()
            print(f"LLM Response: {elapsed_time}")
            st.session_state.messages.append({"role": "user", "content": query})
            st.write(answer_response)
            source=result[0].metadata["source"]
            st.write(f"Source: {source}")
            st.session_state.messages.append({"role": "assistant", "content": answer_response, "context": result[0].metadata["source"]})

