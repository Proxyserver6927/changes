from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


class Loader:
    def __init__(self):
        self.persist_directory = os.getenv('PERSISTANT_STORAGE_DIR')
        self.data_directory = os.getenv('DATA_DIR')
        self.embedding = OpenAIEmbeddings()
    def get_retriever(self):
        if os.path.exists(self.persist_directory):
            choice = input(f"Directory {self.persist_directory} already exists. Do you want to update it? (y/n)")
            if choice.lower() == 'n':
                vectordb = Chroma(persist_directory=self.persist_directory, 
                  embedding_function=self.embedding)


                retriever = vectordb.as_retriever()
                return retriever
        
        # loader = DirectoryLoader(self.data_directory+'/', glob="./*.pdf", loader_cls=PyPDFLoader)
        loader = DirectoryLoader(self.data_directory+'/', glob="./*.md",loader_cls=UnstructuredMarkdownLoader)
        print(loader)
        documents = loader.load()
        print("loaded? ")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print("split? ")
        vectordb = Chroma.from_documents(documents=texts, 
                                        embedding=self.embedding,
                                        persist_directory=self.persist_directory)
        print("persisted? ")

        retriever = vectordb.as_retriever()
        return retriever
        
        


