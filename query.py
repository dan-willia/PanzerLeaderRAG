from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from retrieve import *
import os

os.environ['OPENAI_API_KEY'] = ""

def query_rag(query_text, db, model):
    """
    model is a chat model initialized by init_chat_model like so:
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    """
    PROMPT_TEMPLATE = """
    You are a knowledgeable AI assistant answering questions about the board game Panzer Leader.
    Use the following excerpts from the rules to answer the question.

    {context}

    ---

    Question: {question}
    """
    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    context = construct_context(retrieve_from_chroma(query_text, db))
    prompt = prompt_template.format(context=context, question=query_text)
    response = model.invoke(prompt)
    return response.content
