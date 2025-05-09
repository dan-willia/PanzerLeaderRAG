from langchain_chroma import Chroma
from retrieve import *
import pandas as pd
from utils import *
from rule_hierarchy2 import *
import json

"""
For comparing retrieved node with expected node
"""

data = pd.read_csv("retrieval_testing_edit.csv")
db = Chroma(persist_directory=CHROMA_PATH_2, embedding_function=get_embedding_function())

with open("../DataProcessing/nodes.json", "r") as file:
    tree_rep = json.load(file)
    
tree = create_rule_tree(tree_rep)

for row in range(len(data)):
    query_text = data.iloc[row,0]
    expected_node_tag = data.iloc[row,1]
    retrieved_node_tags = data.iloc[row,2]
    docs = retrieve_from_chroma(query_text, db)
    print("Question:", query_text)
    print("Expected nodes:", expected_node_tag)
    print(get_retrieved_ids(docs))