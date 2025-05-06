from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from query import *
from utils import *
from rule_hierarchy2 import *
import pandas as pd
import os
import json
import random

"""
Command line interface for RAG system; demo uses saved responses so no API key required. 
"""

with open("./nodes.json", "r") as file:
    tree_rep = json.load(file)

tree = create_rule_tree(tree_rep)

qa_data = pd.read_csv("qa_ref.csv")

while True:
    model_choice = int(input("Select model:\n1: 4o-mini\n2: o3-mini\n3: o1-mini\n4: 3.5-turbo\n5: Quit\n"))
    if model_choice == 5:
        break

    db = Chroma(persist_directory=CHROMA_PATH_2, embedding_function=get_embedding_function())

    q_num = random.randint(0,39)
    question = qa_data.iloc[q_num,1]
    response = qa_data.iloc[q_num,model_choice+1]
    print(f"Sample question: {question}\n")
    print(f"Response: {response}")
    docs = retrieve_from_chroma(question, db)
    context = construct_context(docs)
    ids = get_retrieved_ids(tree, docs)
    
    rule_ids = input("Display the relevant rule IDs? (Y/N)\n")
    if rule_ids == "Y":
        print("Rule IDs:", ids)
        
    rules = input("Display the text of the rules? (Y/N)\n")
    if rules == "Y":
        print(context)
    