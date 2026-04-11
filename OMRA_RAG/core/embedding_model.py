from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_embedding_function():
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL"),
        openai_api_base=os.getenv("LM_STUDIO_BASE_URL"),
        openai_api_key="lm-studio",  # <--- MAKE SURE THIS COMMA IS HERE
        check_embedding_ctx_length=False 
    )