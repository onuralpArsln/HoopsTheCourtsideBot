from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("AI_KEY"),
    model_name="gpt-4.1-nano" 
)


embeddings = OpenAIEmbeddings(
    openai_api_key=st.secrets["AI_KEY"],
      model="text-embedding-3-small"  
)