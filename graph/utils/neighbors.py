import networkx as nx
import json
import numpy as np

from graph.models import full_network, Node
from graph.utils.render_subgraph import edge_to_indexed_dictionary


def closed_neighbors(digraph: nx.DiGraph, node_name: str):
    return list(digraph.subgraph(
        nx.all_neighbors(digraph, node_name)).nodes) + [node_name]


def closed_neighborhood(digraph: nx.DiGraph, node_name: str):
    return digraph.subgraph(closed_neighbors(digraph, node_name))
                            
                            
def node_adj(digraph: nx.DiGraph, center: str, other: str, pred=None, succ=None):
    """ can pass in precalculated lists or generators of pred and succ """
    if pred is None:
        pred = list(digraph.predecessors(center))
    if succ is None:
        succ = list(digraph.successors(center))
    output = 0
    if other in succ:
        output += 1
    if other in pred:
        output += 2
    return output
    

def neighborhood_nodes(digraph: nx.DiGraph, node_name: str):
    output = []
    idx = 0
    pred = list(digraph.predecessors(node_name))
    succ = list(digraph.successors(node_name))
    for node in digraph:
        node_dict = {}
        node_dict["name"] = node
        node_dict["index"] = idx
        node_dict["title"] = digraph.nodes[node]["title"]
        node_dict["url"] = digraph.nodes[node]["url"]
        node_dict["adj"] = node_adj(digraph, node_name, node_dict["name"], pred, succ)
        output.append(node_dict)
        idx += 1
    return output


def neighborhood_edges(digraph: nx.DiGraph, node_list, center: str):
    output = []
    for edge in digraph.edges:
        edge_dict = edge_to_indexed_dictionary(edge, node_list)
        if edge[0] == center:
            edge_dict["direction"] = "out"
        elif edge[1] == center:
            edge_dict["direction"] = "in"
        else:
            edge_dict["direction"] = "secondary"
        output.append(edge_dict)
    return output


def neighbor_sentence(center: str, nodes: dict):
    title = Node.objects.get(name=center).title
    n_succ = len(list(full_network.dg.successors(center)))
    n_pred = len(list(full_network.dg.predecessors(center)))
    succ_word = "successor" if n_succ == 1 else "successors"
    pred_word = "predecessor" if n_pred == 1 else "predecessors"
    return f'The article "{title}" links to {n_succ} {succ_word} and is linked to by {n_pred} {pred_word}.'


def render_neighborhood(center: str):
    cn = closed_neighborhood(full_network.dg, center)
    nodes = neighborhood_nodes(cn, center)
    node_dicts = list(nodes)
    edges = neighborhood_edges(cn, nodes, center)
    json_nodes = json.dumps(nodes, ensure_ascii=False)
    json_edges = json.dumps(edges, ensure_ascii=False)
    sentence = neighbor_sentence(center, nodes)
    return json_nodes, json_edges, sentence, node_dicts


