# from langchain.text_splitter import CharacterTextSplitter, MarkdownHeaderTextSplitter
# from langchain.document_loaders import AsyncChromiumLoader
# from langchain.document_transformers import Html2TextTransformer
# from langchain.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# import nest_asyncio

# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate
# from langchain_openai import OpenAI
# from langchain.schema.runnable import RunnablePassthrough

from src.scrapper import ScrapeWebPage
from src.add_image_markdown import get_content



# nest_asyncio.apply()

urls = "https://tai.com.np/"
url_scrapper = ScrapeWebPage(urls)
url_list = url_scrapper.get_url()

articles = [url for url in url_list[0] if url.startswith(urls)]
##remove dub urls
cleaned_urls = []
print()
articles = [cleaned_urls.append(url) for url in articles if url not in cleaned_urls]
print(cleaned_urls)
print()


# headers_to_split_on = [
#     ("#", "Header 1"),
#     ("##", "Header 2"),
#     ("###", "Header 3"),
# ]
# mardown_text = get_content(url=urls)
# markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
# md_header_splits = markdown_splitter.split_text(mardown_text)

# # Chunk text
# # text_splitter = CharacterTextSplitter(chunk_size=512, 
# #                                       chunk_overlap=0)
# # chunked_documents = text_splitter.split_documents(docs_transformed)

# # Load chunked documents into the FAISS index
# db = FAISS.from_documents(md_header_splits, 
#                           HuggingFaceEmbeddings(model_name="sentence-transformers/msmarco-distilbert-base-v3"))




# # _standalone_prompt = """Given the following query 
# # ###Question:
# # {question}
# # rephrase the question to be a standalone question, in its original language, 
# # that can be used to query a FAISS index. This query will be used to retrieve documents with additional context.
# # Give be the 5 rephrased question, format your answer in json object like.
# # '
# #   "0":"rephrased question 0",
# #   "1":"rephrased question 1",
# #   "2":"rephrased question 2",
# #   "3":"rephrased question 3",
# #   "4":"rephrased question 4",
# # '
# # """

# # prompt = PromptTemplate(
# #     input_variables=["question"],
# #     template=_standalone_prompt,
# # )


# # llm = OpenAI(openai_api_key="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")
# # llm_chain = LLMChain(prompt=prompt, llm=llm)

# # svalues=llm_chain.invoke(input="who is cto of TAI?")


# # import json
# # json_values = json.loads(svalues["text"])

# # retrivals_chunks = []
# # for i in range(len(json_values)):
# #   print(json_values["{}".format(i)])
# #   retrival = db.similarity_search(json_values["{}".format(i)], k=2)
# #   retrivals_chunks.append(retrival)

# # print(retrivals_chunks)


# # for i in retrivals_chunks:
# #   print(i[0].page_content)
# #   print()


# # Connect query to FAISS index using a retriever
# retriever = db.as_retriever(
#     search_type="similarity",
#     search_kwargs={'k': 1}
# )

# prompt_template = """ CONTEXT: {context}
#     You are a helpful assistant, above is some context, 
#     Please answer the question, and make sure you follow ALL of the rules below:
#     1. Answer the questions only based on context provided, do not make things up
#     2. Answer questions in a helpful manner that straight to the point, with clear structure & all relevant information that might help users answer the question
#     3. Anwser should be formatted in Markdown
#     4. If there are relevant images, video, links, they are very important reference data, please include them as part of the answer

#     QUESTION: {question}
#     ANSWER (formatted in Markdown):
    
# """

# prompt = PromptTemplate(
#     input_variables=["context", "question"],
#     template=prompt_template,
# )

# llm = OpenAI(openai_api_key="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")
# llm_chain = LLMChain(prompt=prompt, llm=llm)


# query = "who is chief technology officer of tai?" 

# # print(db.similarity_search(query, k=4))
# # retriever = db.as_retriever()

# rag_chain = ( 
#  {"context": retriever, "question": RunnablePassthrough()}
#     | llm_chain
# )

# print(rag_chain.invoke(query))


from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
import requests
import json
import os
import html2text
from langchain.chat_models import ChatOpenAI
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser, MarkdownNodeParser
from llama_index.core.text_splitter import TokenTextSplitter
from langchain.prompts import ChatPromptTemplate
from llama_index.core import VectorStoreIndex
from langchain.embeddings import HuggingFaceEmbeddings
import openai

load_dotenv()
brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# 1. Scrape raw HTML

def scrape_website(url):
    html_content = requests.get(url)
    return html_content.text

# 2. Convert html to markdown

def convert_html_to_markdown(html):

    # Create an html2text converter
    converter = html2text.HTML2Text()

    # Configure the converter
    converter.ignore_links = False

    # Convert the HTML to Markdown
    markdown = converter.handle(html)

    return markdown


# Turn https://developers.webflow.com/docs/getting-started-with-apps to https://developers.webflow.com

def get_base_url(url):
    parsed_url = urlparse(url)

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


# Turn relative url to absolute url in html

def convert_to_absolute_url(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    for img_tag in soup.find_all('img'):
        if img_tag.get('src'):
            src = img_tag.get('src')
            if src.startswith(('http://', 'https://')):
                continue
            absolute_url = urljoin(base_url, src)
            img_tag['src'] = absolute_url
        elif img_tag.get('data-src'):
            src = img_tag.get('data-src')
            if src.startswith(('http://', 'https://')):
                continue
            absolute_url = urljoin(base_url, src)
            img_tag['data-src'] = absolute_url

    for link_tag in soup.find_all('a'):
        href = link_tag.get('href')
        if href.startswith(('http://', 'https://')):
            continue
        absolute_url = urljoin(base_url, href)
        link_tag['href'] = absolute_url

    updated_html = str(soup)

    return updated_html


def get_markdown_from_url(url):
    # base_url = get_base_url(url)

    # print(f"Processing: {url}")
    html = scrape_website(url)
    updated_html = convert_to_absolute_url(html, url)
    markdown = convert_html_to_markdown(updated_html)
    
    return markdown


# 3. Create vector index from markdown

def create_index_from_text(markdown):
    text_splitters = TokenTextSplitter(
        separator="",
        chunk_size=1024,
        chunk_overlap=20,
        backup_separators=["\n\n", ".", ","]
    )

    node_parser = MarkdownNodeParser.from_defaults()
                    
    nodes = node_parser.get_nodes_from_documents(
        markdown, show_progress=True)

    # build index
    index = VectorStoreIndex(nodes)

    print("Index created!")
    return index


# 4. Retrieval Augmented Generation (RAG)


def generate_answer(query, index):

    # Get relevant data with similarity search
    retriever = index.as_retriever()
    nodes = retriever.retrieve(query)
    texts = [node.node.text for node in nodes]

    print("Retrieved texts!", texts)

    # Generate answer with OpenAI
    model = ChatOpenAI(model_name="gpt-3.5-turbo")
    template = """
    CONTEXT: {docs}
    You are a helpful assistant, above is some context, 
    Please answer the question, and make sure you follow ALL of the rules below:
    1. Answer the questions only based on context provided, do not make things up
    2. Answer questions in a helpful manner that straight to the point, with clear structure & all relevant information that might help users answer the question
    3. Anwser should be formatted in Markdown
    4. If there are relevant images, video, links, they are very important reference data, please include them as part of the answer

    QUESTION: {query}
    ANSWER (formatted in Markdown):
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    response = chain.invoke({"docs": texts, "query": query})

    return response.content


# url = "https://tai.com.np/team"
query = "who is cto of tai?"

docs = []
print(cleaned_urls)
for url in cleaned_urls:
    print(url)
    markdown = get_markdown_from_url(url)
    # print(markdown)
    docs.append(Document(text=markdown))

index = create_index_from_text(docs)

# print(len(docs))

answer = generate_answer(query, index)
print(answer)