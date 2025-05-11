import pypdf
import json
import re
import argparse

"""
Converts rules into dict with section title as key and section text as value

KNOWN ISSUES:
- Section XIII.A has identical heading to Section IV.A, causing section XIII to be placed
  under Section XII. The current solution is to edit the outputed nodes.json file manually,
  adding "A. ALLIED PLAYER SEGMENT. " (the '.' ensures uniqueness) in the appropriate section.
- A similar issue applies to XIII.B, but it only results in XIII.B missing from the output.
  "B. GERMAN PLAYER SEGMENT. " is added manually to nodes.json.
- For rules VII.G.1, IX.B.1, and IX.C.1, a similar issue occurs, where these rules are not 
  included in the output because of duplicate keys. The same solution of manually entering the
  data is applied.
  
In future, we can address this issue by adding a tag to duplicate keys. For now, note that
creating a new json will overwrite the previous one, and thus not contain the complete rules.

"""
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

def parse_args():
    parser = argparse.ArgumentParser(description='Process rules from PDF and optionally output to JSON')
    parser.add_argument('--output-json', '-o', action='store_true',
                        help='Output the processed rules to a JSON file')
    parser.add_argument('--print-dict', '-p', action='store_true',
                        help='Print the dictionary keys to console')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    nodes = process_rules(reader)
    
    if args.print_dict:
        for k,v in nodes.items():
            print(k)
        
    if args.output_json:
        with open("nodes.json", "w") as f:
            json.dump(nodes, f)