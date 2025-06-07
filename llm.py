from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("AI_KEY"),
    model_name="gpt-4.1-nano" 
)