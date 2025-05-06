# Get all children of a node
def get_children(node):
    children = []
    for child in node.children:
        get_children_recursive(child, children)
    return children

def get_children_recursive(node, children):
    for child in node.children:
        children.append(child)
        return get_children_recursive(child, children)
    return children

def print_nodes(node):
    """
    Print node and all its children.
    """
    print(node.id, node.description)
    for children in node.children:
        print_nodes(children)
        
def get_node_from_node(node, search_id):
    # Searches for search_id in node and all children
    if node.id == search_id:
        return node
    else:
        for child in node.children:
            node = get_node_from_node(child, search_id)
            if node:
                return node
            
def get_node_from_tree(tree, search_id):
    for node in tree:
        node = get_node_from_node(node, search_id)
        if node:
            return node
        
def get_ancestors(node):
    """
    Returns list of ancestors in top-down order as a list of nodes
    """
    ancestors = []
    cur_parent = node.parent
    while cur_parent:
        ancestors.append(cur_parent)
        cur_parent = cur_parent.parent
    ancestors.reverse()
    return ancestors

def get_tag(node):
    """
    Return the tag of a rule (e.g. VII.J.8)
    """
    idx = node.id.find('.')
    if idx == -1:
        idx = node.id.find(')')
    tag = node.id[:idx]
    cur_parent = node.parent
    while cur_parent:
        idx = cur_parent.id.find('.')
        tag = cur_parent.id[:idx+1] + tag
        cur_parent = cur_parent.parent
    return tag

def find_node_recursive(node, node_id: str):
    if node.id.rstrip() == node_id.rstrip():
        return node
    else:
        if node.children:
            for child in node.children:
                node = find_node_recursive(child, node_id)
                if node:
                    return node

def find_node(tree, node_id: str):
    for node in tree:
        node = find_node_recursive(node, node_id)
        if node:
            return node
        
def get_retrieved_ids(tree, docs):
    retrieved_ids = []
    for doc in docs:
        path = doc.metadata['path']
        node = find_node(tree, path)
        tag = get_tag(node)
        retrieved_ids.append(tag)
    return retrieved_ids