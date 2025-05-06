from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.schema import Document
import re
import json
import os
import shutil

"""
Creates the vector embedding database from the JSON representation of rules. 
"""

global CHROMA_PATH_2
CHROMA_PATH_2 = "./ChromaDB_2/"

def vectorize_rule_json(rule_json):
    """
    Convert a JSON rule structure into chunks for vectorization and add them to Chroma.
    """
    chunks = []

    def process_rule_node(node_dict, path=None):
        if path is None:
            path = []

        # Create chunks for the current rules
        for key, value in node_dict.items():
            # Skip empty values
            if not value and not isinstance(value, dict):
                continue

            current_path = path + [key]
            full_path = " > ".join(current_path)

            # Create document for this rule
            if isinstance(value, str) and value.strip():
                chunk = Document(
                    page_content=value.strip(),
                    metadata={
                        "source": "rules_json",
                        "rule": key.strip(),
                        "path": full_path,
                        "level": len(current_path)
                    }
                )
                chunks.append(chunk)

            if isinstance(value, dict):
                process_rule_node(value, current_path)

    # Start processing from the root
    process_rule_node(rule_json)

    # Calculate unique IDs for each chunk
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add to Chroma
    add_to_chroma(chunks_with_ids)

    return chunks_with_ids

def calculate_chunk_ids(chunks):
    """
    Calculate unique IDs for rule chunks based on their path in the rule hierarchy.
    """
    for i, chunk in enumerate(chunks):
        # Create an ID based on the rule path, cleaned up for use as an ID
        path = chunk.metadata.get("path", "")
        # Clean path to make it suitable for an ID
        clean_path = re.sub(r'[^\w\s>]', '', path).replace(' ', '_').replace('>', '-')
        chunk_id = f"rule:{clean_path}"

        # Add the ID to metadata
        chunk.metadata["id"] = chunk_id

    return chunks

def get_embedding_function():
    embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    return embeddings

def add_to_chroma(chunks):
    """
    Add document chunks to Chroma vector database.

    Args:
        chunks: List of Document objects with metadata including IDs
    """
    # Load database
    db = Chroma(persist_directory=CHROMA_PATH_2, embedding_function=get_embedding_function())

    # Get existing IDs from the database
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB
    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add")

    return db

def clear_database():
    if os.path.exists(CHROMA_PATH_2):
        shutil.rmtree(CHROMA_PATH_2)

def main():
    with open("./data/nodes.json", "r") as file:
        data = json.load(file)
    vectorize_rule_json(data)
    
if __name__ == '__main__':
    main()