# PanzerLeaderRAG

Implements a QA system enhanced by retrieval augmented generation (RAG) for the rulebook of the Avalon Hill game [Panzer Leader](https://en.wikipedia.org/wiki/Panzer_Leader_(game)).

The architecture of the application is shown below, and is explained in more detail in the [project report](/FinalProjectReport.pdf).

![project architecture](/architecture.png)

## Project features
- Full RAG pipeline from preprocessing to answer generation
  - Creation of vector embedding database of game rules 
  - Cosine similarity calculation between query and rules for retrieval
  - API calls via LangChain to OpenAI models for generation
- Creation of evaluation framework based on related work research
- Performance evaluation of four different LLMs

**Created as final project for Natural Language Processing at CU Boulder in Spring 2025**

## Files and folders

`/DataProcessing/` contains scripts and data for parsing the PDF of the rulebook, vectorizing the rules, and storing them in a ChromaDB.

`/ChromaDB_2/` is a database of the vectorized embeddings so that the demo doesn't need to re-vectorize the entire rulebook.

`/Generate/` contains code for generating responses to 40 test questions from four OpenAI LLMs. 

`/Evaluate/` contains code and data related to evaluating the retrieved rules and generated responses.

`FinalProjectReport.pdf` contains the project writeup including research on related work.

## Dependencies

- `langchain==0.3.25 `

- `langchain_community==0.3.23`

- `langchain_core==0.3.58`

- `pandas==2.2.3`

- `pypdf==5.4.0`

## Demo

`demo.py` contains a command line interface of the system. It will ask for an OpenAI API key.

`demo_nokey.py` can be used to access a demo without an OpenAI API key. Random queries from the evaluation set are chosen, and saved answers from the evaluation study are retrieved. 

