from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model="local-model",  # LM Studio ignores this
        openai_api_base=os.getenv("LM_STUDIO_BASE_URL"),
        openai_api_key="lm-studio",
        temperature=0.7
    )

def generate_answer(question: str, context_chunks: list) -> str:
    # Combine context
    context_text = "\n\n".join([chunk.page_content for chunk, _ in context_chunks])
    
    # Create prompt
    prompt_template = ChatPromptTemplate.from_template(
        """You are a helpful assistant. Answer the question based on the context provided.
The context may contain structured data in JSON format - extract the relevant information and provide a natural, conversational answer.

Context:
{context}

Question: {question}

Provide a clear, direct answer in natural language. Do not include JSON formatting, decision structures, or technical metadata in your response."""
    )
    
    llm = get_llm()
    prompt = prompt_template.format(context=context_text, question=question)
    
    response = llm.invoke(prompt)
    return response.content
