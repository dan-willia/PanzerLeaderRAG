import pypdf
import Node
import json
import re

"""
Converts rules into dict with section title as key and section text as value
"""

OUTPUT_JSON = False
PRINT_DICT = False

reader = pypdf.PdfReader("plrules.pdf")

def process_rules(reader):
    nodes = dict()
    romnum = r'\b(XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\.\s'
    
    # process page
    cur_key = ''
    for obj in reader.pages:
        # process lines
        lines = obj.extract_text().split('\n')
        for line in lines:
            # print(line)
            # skip first line of rulebook
            if line == 'RULES OF PLAY ':
                continue
            # skip if line is empty
            if line == ' ':
                continue
            # if there's a roman numeral, then extract the line
            if re.search(romnum, line):
                nodes[line] = ''
                # print(f"EXTRACTED SECTION TITLE: {page[i]}")
                cur_key = line
                # SUGGEST: cur_key = line[:-1] 
                # REASON: TO REMOVE TRAILING WHITE SPACE
            # check the first two chars
            elif line[0].isalnum() and (line[1] == '.' or line[1] == ')' or (line[1].isalnum() and line[2] == '.')):
                # to prevent '3),' from invalidly slipping through
                if line[2] == ',':
                    continue
                nodes[line] = ''
                cur_key = line
                # print(f"EXTRACTED SECTION TITLE: {page[i]}")
            # add line to node
            else:
                # print(line)
                nodes[cur_key] += line
    return nodes

nodes = dict()
romnum = r'\b(XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)[.]\b'
lines = reader.pages[13].extract_text().split('\n')
cur_key = ''
for line in lines:
    # print(line)
    # skip first line of rulebook
    if line == 'RULES OF PLAY ':
        continue
    # skip if line is empty
    if line == ' ':
        continue
    # if there's a roman numeral, then extract the line
    if re.search(romnum, line):
        nodes[line] = ''
        # print(f"EXTRACTED SECTION TITLE: {page[i]}")
        cur_key = line
    # check the first two chars
    elif line[0].isalnum() and (line[1] == '.' or line[1] == ')' or (line[1].isalnum() and line[2] == '.')):
        # to prevent '1),' from invalidly slipping through
        if line[2] == ',':
            continue
        nodes[line] = ''
        cur_key = line
        print(f"EXTRACTED SECTION TITLE: {line}")
    # add line to node
    else:
        # print(line)
        if cur_key == '':
            continue
        nodes[cur_key] += line

nodes = process_rules(reader)

if PRINT_DICT:
    for k,v in nodes.items():
        print(k)
    
if OUTPUT_JSON:
    with open("nodes.json", "w") as f:
        json.dump(nodes, f)