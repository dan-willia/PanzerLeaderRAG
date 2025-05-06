from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from query import *
import pandas as pd
import os

"""
Generates answers to 40 test questions for four OpenAI models
Writes output to csv "
"""

OPENAI_API_KEY = ""
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

TEST_QUESTIONS_PATH = "./question_answers2.csv"
OUTPUT_PATH = "../Evaluate/qa_ref.csv"

RUN_TEST = False
OUTPUT_CSV = False

gpt4o_mini = init_chat_model("openai:gpt-4o-mini")
o3_mini = init_chat_model("openai:o3-mini")
o1_mini = init_chat_model("openai:o1-mini")
gpt3_5turbo = init_chat_model("openai:gpt-3.5-turbo")

models = [gpt4o_mini, o3_mini, o1_mini, gpt3_5turbo]
# models = ["gpt4o_mini", "o3_mini", "o1_mini", "gpt3_5turbo"]

qa_ref = pd.read_csv(TEST_QUESTIONS_PATH)

db = Chroma(persist_directory=CHROMA_PATH_2, embedding_function=get_embedding_function())

qa_ref["4o-mini"] = None
qa_ref["o3-mini"] = None
qa_ref["o1-mini"] = None
qa_ref["3.5 Turbo"] = None

def run_test():
    for model_i in range(len(models)):
        model = models[model_i]
        for row in range(len(qa_ref)):
            query = qa_ref.iloc[row,0]
            response = query_rag(query, db, model)
            # response = model + " answer for q: " + query
            qa_ref.iloc[row,model_i+2] = response
            
if RUN_TEST:
    run_test()

if OUTPUT_CSV:
    qa_ref.to_csv(OUTPUT_PATH)