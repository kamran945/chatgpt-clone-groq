import os

from langchain_groq.chat_models import ChatGroq
from langchain_ollama import ChatOllama


llm = ChatGroq(
    model=os.getenv("CHAT_GROQ_MODEL"),
    stop_sequences="[end]",
    temperature=0.0,
)
