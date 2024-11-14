import pinecone
import openai
from dotenv import load_dotenv
import os
from pinecone.grpc import PineconeGRPC

pc = PineconeGRPC(api_key=os.environ['PINECONE_API_KEY'])

# From here on, everything is identical to the REST-based client.
index = pc.Index(host=os.environ['PINECONE_HOST'])

# index.upsert(vectors=[])
# index.query(vector=[...], top_key=10)
load_dotenv()
openai.api_key= os.environ["OPENAPI_KEY"]

pinecone.init(api_key=os.environ["PINECONE_KEY"], environment="gcp-starter")
pinecone


class PineconeStore:
    def __init__(self, embeddings, dataset):
        self.embeddings = embeddings
        self.dataset = dataset
    
    def _create_embeddings_for_data(self):
        from sentence_transformers import SentenceTransformer
        import torch
        device = "cuda" if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer('sentence-transformers/msmarco-distilbert-base-v3"')