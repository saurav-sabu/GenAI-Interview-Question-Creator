from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from prompt import *

from dotenv import load_dotenv
import os


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def file_processing(file_path):

    loader = PyPDFDirectoryLoader(file_path)
    data = loader.load()

    question_data = ""
    for page in data:
        question_data += page.page_content


    splitter = TokenTextSplitter(
    model_name= "gpt-3.5-turbo",
    chunk_size = 10000,
    chunk_overlap = 200
    )

    chunk = splitter.split_text(question_data)

    document_data = [Document(page_content=text) for text in chunk]

    splitter_answer = TokenTextSplitter(
    model_name= "gpt-3.5-turbo",
    chunk_size = 1000,
    chunk_overlap = 100
    )

    chunk_answer = splitter_answer.split_documents(document_data)

    return  document_data , chunk_answer 



def initialize_llm_pipeline(file_path):

    document_data , chunk_answer = file_processing(file_path)

    llm = ChatOpenAI(model="gpt-3.5-turbo",
                 temperature=0.4,
                )

    question_prompt = PromptTemplate(template = prompt_template,input_variables=["text"])

    Refine_question_prompt = PromptTemplate(
    input_variables =  ["existing_answer","text"],
    template = refine_template
    )

    chain = load_summarize_chain(
    llm = llm,
    chain_type="refine",
    question_prompt = question_prompt,
    refine_prompt = Refine_question_prompt
    )

    query = chain.run(chunk_answer)

    embedding = OpenAIEmbeddings()

    vector_store = FAISS.from_documents(chunk_answer,embedding)

    llm_answer  = ChatOpenAI(temperature=0.3,model="gpt-3.5-turbo")

    query = query.split("\n")

    answer_chain = RetrievalQA.from_chain_type(
    llm = llm_answer,
    chain_type="stuff",
    retriever = vector_store.as_retriever()
    )

    return answer_chain, query




