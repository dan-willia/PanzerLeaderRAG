from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from Generate.query import *
from DataProcessing.utils import *
from DataProcessing.rule_hierarchy2 import *
import pandas as pd
import os
import json

"""
Command line interface for RAG system.
"""

OPENAI_API_KEY = input("Enter OPENAI_API_KEY\n")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

gpt4o_mini = init_chat_model("openai:gpt-4o-mini")
o3_mini = init_chat_model("openai:o3-mini")
o1_mini = init_chat_model("openai:o1-mini")
gpt3_5turbo = init_chat_model("openai:gpt-3.5-turbo")

models = [gpt4o_mini, o3_mini, o1_mini, gpt3_5turbo]

with open("./DataProcessing/nodes.json", "r") as file:
    tree_rep = json.load(file)

tree = create_rule_tree(tree_rep)

while True:
    model_choice = int(input("Select model:\n1: 4o-mini\n2: o3-mini\n3: o1-mini\n4: 3.5-turbo\n5: Quit\n"))
    if model_choice == 5:
        break
    model = models[model_choice-1]

    db = Chroma(persist_directory=CHROMA_PATH_2, embedding_function=get_embedding_function())

    question = input("Enter a question: (sample question: What is the time scale in PANZER LEADER, and what does each turn represent?)\n")

    response = query_rag(question, db, model)
    print(response)
    docs = retrieve_from_chroma(question, db)
    context = construct_context(docs)
    ids = get_retrieved_ids(tree, docs)
    
    rule_ids = input("Display the relevant rule IDs? (Y/N)\n")
    if rule_ids == "Y":
        print("Rule IDs:", ids)
        
    rules = input("Display the text of the rules? (Y/N)\n")
    if rules == "Y":
        print(context)
    