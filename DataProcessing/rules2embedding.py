import os
os.environ["TOKENIZERS_PARALLELISM"] =  "false"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from rule_hierarchy2 import create_rule_tree
from utils import find_node, get_tag
import json
import shutil

"""
Creates the vector embedding database from the JSON representation of rules. 
"""

global CHROMA_PATH_2
CHROMA_PATH_2 = "../ChromaDB_2/"

def vectorize_rule_json(rule_json):
    """
    Convert a JSON rule structure into chunks for vectorization and add them to Chroma.
    """
    chunks = []

    tree = create_rule_tree(rule_json)

    def process_rule_node(node_dict):
        # Create chunks for the current rules
        for key, value in node_dict.items():
            node = find_node(tree, key)
            tag = get_tag(node)
            # print(tag)

            # Create document for this rule
            if value.strip():
                chunk = Document(
                    page_content=value.strip(),
                    metadata={
                        "source": "rules_json",
                        "rule": key.strip(),
                        "tag": tag,
                    }
                )
                chunks.append(chunk)

    # Start processing from the root
    process_rule_node(rule_json)

    # Add to Chroma
    add_to_chroma(chunks)

    # return chunks_with_ids
    return chunks

def get_embedding_function():
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    return embeddings

def add_to_chroma(chunks):
    """
    Add document chunks to Chroma vector database.

    Args:
        chunks: List of Document objects with metadata including IDs
    """
    # Load database
    db = Chroma(persist_directory=CHROMA_PATH_2, embedding_function=get_embedding_function())

    # Get existing tags from the database
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB
    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["tag"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_tags = [chunk.metadata["tag"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_tags)
    else:
        print("No new documents to add")

    return db

def clear_database():
    if os.path.exists(CHROMA_PATH_2):
        shutil.rmtree(CHROMA_PATH_2)

def main():
    with open("./nodes.json", "r") as file:
        data = json.load(file)
    vectorize_rule_json(data)

if __name__ == '__main__':
    main()