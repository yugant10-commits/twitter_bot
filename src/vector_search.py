from langchain.text_splitter import CharacterTextSplitter, MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import getpass
import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY =os.environ["OPENAI_API_KEY"]
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
class VectorSearch:
    def __init__(self, data:list, model_name:str) -> None:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        self.data = data
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings(model=model_name, openai_api_key=OPENAI_API_KEY)
        # self.embeddings = HuggingFaceEmbeddings(model_name = self.model_name)
    
    def _split_data(self):
        text_splitter = CharacterTextSplitter(chunk_size=1500, separator='/n')
        self.docs, self.metadatas = [], []
        for page in self.data:
            splits = text_splitter.split_text(page['text'])
            self.docs.extend(splits)
            self.metadatas.extend([{"source": page['source']}] * len(splits))
        return self.docs, self.metadatas
    
    def _split_data_markdown(self):

        text_splitter = CharacterTextSplitter(chunk_size=1500, separator='/n')
        self.docs, self.metadatas = [], []
        for page in self.data:
            splits = text_splitter.split_text(page['text'].lower())
            # print(splits)
            self.docs.extend(splits[0].page_content)
            self.metadatas.extend([{"source": page['source']}] * len(splits))
        return self.docs, self.metadatas
    
    def _faiss_search(self):
        store = FAISS.from_texts(self.docs, self.embeddings, metadatas=self.metadatas)
        return store



        
        
    
        
