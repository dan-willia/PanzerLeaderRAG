import os
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

from langchain_huggingface import HuggingFaceEmbeddings

global CHROMA_PATH_2
CHROMA_PATH_2 = "../ChromaDB_2/"

def retrieve_from_chroma(query_text, db, k_results=3):
    """
    Retrieve the most relevant rule chunks for a given query.

    Args:
        query_text: The text query to search for
        n_results: Number of results to return
        db: Chroma database

    Returns:
        List of Document objects
    """
    results = db.similarity_search_with_score(query=query_text,k=3)
    return [doc for doc,score in results]
    
def construct_context(retrieved_docs):
    context = ""
    for doc in retrieved_docs:
        context += doc.metadata['rule'] + ': '
        context += doc.page_content + '\n'
    return context

def get_embedding_function():
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    return embeddings