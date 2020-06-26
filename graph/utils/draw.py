import json 

import networkx as nx

from network import Network
from subgraph import induced_subgraph, n_shortest_paths

sep = Network.from_jl('related.jl', 'related')
subg = induced_subgraph(sep.dg, 'aristotle', 'nietzsche')
# TODO: (IN VEGA SPEC): Add signal for transforms (to hide behind css)
def json_node_list(graph, source, target):
    output = []
    idx = 0
    for node in graph.nodes:
        node_dict = {}
        node_dict["name"] = node
        node_dict["index"] = idx
        node_dict["title"] = graph.nodes[node]["title"]
        node_dict["url"] = graph.nodes[node]["url"]
        node_dict["steps"] = n_shortest_paths(graph, source, node)[1] - 1
        output.append(node_dict)
        idx += 1
    return output

def json_edge_list(graph, node_list):
    output = []
    for edge in graph.edges:
        output.append(edge_to_indexed_dictionary(edge, node_list))
    return output
        
def edge_to_indexed_dictionary(edge: tuple, node_list: list):
    source_idx = list(filter(lambda x: x['name'] == edge[0], node_list))[0]['index']
    target_idx = list(filter(lambda x: x['name'] == edge[1], node_list))[0]['index']
    return {"source": source_idx, "target": target_idx}

def vega_json(graph, source, target):
    nodes = json_node_list(graph, source, target)
    edges = json_edge_list(graph, nodes)
    vega_dict = {"nodes": nodes, "links": edges}
    vega_dict["directed"] = type(graph) == nx.classes.digraph.DiGraph
    return json.dumps(vega_dict, ensure_ascii=False)