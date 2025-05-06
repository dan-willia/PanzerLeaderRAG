demo.py contains a command line interface demo of the system. It will ask for an OpenAI API key.

To run a "fake" demo without needing to input a key, run demo_nokey.py instead.

Dependencies:

langchain==0.3.25 

langchain_community==0.3.23

langchain_core==0.3.58

pandas==2.2.3

pypdf==5.4.0

Files and folders:

DataProcessing contains scripts and data for parsing the PDF of the rulebook, vectorizing the rules, and storing them in a ChromaDB.
It also contains the Node class which is used to represent the structure of the rules. 

ChromaDB_2 is a database of the vectorized embeddings of the rules so that the demo doesn't need to re-vectorize the entire rulebook.

Generate contains code for generating responses to 40 test questions from four OpenAI LLMs. 

Evaluate contains code and data related to evaluating the retrieved rules and generated responses.

demo.py and demo_nokey.py are demos of the system. 
