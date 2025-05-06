import json
import Node
import re

def create_rule_tree(rules_json):
    """
    Returns a list of Nodes which represents the rule tree for Panzer Leader.
    """
    tree = []
    romnum = r'\b(XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\.\s'

    for k,v in rules_json.items():
        # Level 1: Roman Numerals
        if re.search(romnum, k) and "DETERMINE" not in k: # second clause to block I. when it's a letter and not a romnum
            cur_top_level = Node.Node(id=k,description=v)
            tree.append(cur_top_level)
        # Level 2: Capital letters
        elif k[0].isupper() and k[1] == '.':
            cur_2nd_level = Node.Node(id=k,description=v)
            cur_top_level.add_child(cur_2nd_level)
        # Level 3: Arabic numerals
        elif k[0].isnumeric():
            cur_3rd_level = Node.Node(id=k,description=v)
            cur_2nd_level.add_child(cur_3rd_level)
        # Level 4: Lower case letters
        else:
            cur_4th_level = Node.Node(id=k,description=v)
            cur_3rd_level.add_child(cur_4th_level)

    return tree