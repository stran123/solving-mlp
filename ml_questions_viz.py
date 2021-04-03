import networkx as nx
import matplotlib.pyplot as plt
import json
# import pydot
# from networkx.drawing.nx_pydot import *

# import os
# os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'


OPS = ['+', '-', '*', '/', '^', 'l', 'm']

class TreeNode:
    
    def __init__(self, key, parent, token):
        self.key = key
        self.parent = parent
        self.token = token
        self.left = None
        self.right = None
    
    def layout(self, depth, min_pos, max_pos, pos_dict, inv_pos_dict):
        avg = 0.5*(min_pos + max_pos)
        pos_dict[self.key] = (avg, -depth)
        inv_pos_dict[(avg, -depth)] = self.key
        if self.left:
            self.left.layout(depth + 1, min_pos, avg, pos_dict, inv_pos_dict)
        if self.right:
            self.right.layout(depth + 1, avg, max_pos, pos_dict, inv_pos_dict)
    
    def build_nx(self, graph):
        graph.add_node(self.key, token=self.token)
        if self.parent:
            graph.add_edge(self.parent.key, self.key)
        if self.left:
            self.left.build_nx(graph)
        if self.right:
            self.right.build_nx(graph)
    
    def move_nodes(self, pos_dict):
        if self.left:
            self.left.move_nodes(pos_dict)
            self.right.move_nodes(pos_dict)
            pos_dict[self.key] = (0.5*(pos_dict[self.left.key][0] + pos_dict[self.right.key][0]) ,pos_dict[self.key][1])

def build_tree(tokens, key):
    parent = None
    root = None
    for i, token in enumerate(tokens):
        print(token)
        node = TreeNode(i + key, parent, token)
        if i == 0:
            root = node
        if parent:
            if parent.left:
                print("Right")
                parent.right = node
            else:
                print("Left")
                parent.left = node
        if token in OPS or not parent:
            print("OPS")
            parent = node
        else:
            while parent and parent.right:
                print("Up")
                parent = parent.parent
                if parent and not parent.parent and parent.right:
                    return parent, key + i
    while parent and parent.right:
        parent = parent.parent
        if not parent.parent:
            return parent, key + len(tokens)
    return root, key + len(tokens)

            

def construct_graphic(tokens, name):
    
    key = 0
    graph = nx.Graph()

    root, key = build_tree(tokens, key)

    pos = {}
    inv_pos = {}
    root.layout(0, 0, len(tokens), pos, inv_pos)
    
    sorted_list = sorted(inv_pos.keys())
    sorted_keys = [inv_pos[x] for x in sorted_list]

    pos = {key: (i, pos[key][1]) for i, key in enumerate(sorted_keys)}

    root.move_nodes(pos)

    # pos = pydot_layout(graph, prog="dot")
    
    root.build_nx(graph)
    print(graph.nodes)

    token_dict = nx.get_node_attributes(graph, 'token')
    nx.draw(graph, pos, labels=token_dict, arrows=False)
    plt.savefig(name)
    plt.close()