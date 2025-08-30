import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = TextLoader("Data/example.txt", autodetect_encoding=True)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)  
manual_documents = text_splitter.split_documents(documents)

embeddings = OllamaEmbeddings(model="bge-m3")

vectorstore = FAISS.from_documents(manual_documents, embeddings)

def query(context: str):
    return vectorstore.similarity_search(context, k=1)

if __name__ == "__main__":
    pass
