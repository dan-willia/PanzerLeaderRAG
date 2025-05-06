import re

class Node:
    def __init__(self, id: str, description=""):
        self.id = id
        self.description = description
        self.children = []
        self.parent = None
        self.references = []
        # self.type = "" # type is {PRIM, SEC, TERT, QUAT}

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)
		
    def add_parent(self, parent_node):
        self.parent = parent_node
        if self not in parent_node.children:
            parent_node.add_child(self)

    def add_reference(self, target_node):
        self.references.append(target_node)

    def add_description(self, description):
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "children": [child.to_dict() for child in self.children],
            "references": [ref.id for ref in self.references]
        }
    
    def __str__(self):
        return f"{self.id} {self.description}"