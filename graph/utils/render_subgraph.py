import random

import networkx as nx

from graph.models import full_network, Node
from graph.utils.subgraph import directed_induced_subgraph, n_shortest_paths, all_shortest_paths, result_string


NO_PATH_STRINGS = [("No path found! Here's your next paper title: "
                    '"The Surprising Path from {} to {}"'),
                   ("No path found! It's up to you to figure out "
                    "how to get from {} to {}."),
                   ("Couldn't find a path! Try it in reverse!"),
                   ("No path found! Try an undirected search below.")] 


def results(source, target, is_undirected):
    try:
        nw = full_network.g if is_undirected else full_network.dg
        subgraph = directed_induced_subgraph(nw, source, target)
        sentence = result_string(subgraph, source, target)
        paths = list(all_shortest_paths(subgraph, source, target))
        friendly_paths = get_friendly_paths(paths)
        render_vega = True
        if is_undirected:
            json_data_path = f"{source}_subgdata_{target}.json"
        else:
            json_data_path = f"{source}_subdgdata_{target}.json"
    except nx.exception.NetworkXNoPath:
        source_title = Node.objects.get(name=source).title
        target_title = Node.objects.get(name=target).title
        sentence = random.choice(NO_PATH_STRINGS)
        sentence = sentence.format(source_title, target_title)
        friendly_paths = []
        render_vega = False
        json_data_path = ""
    results_package = (sentence, friendly_paths, render_vega, json_data_path)
    return results_package

def get_friendly_paths(paths):
    outerlist = []
    for path in paths:
        innerlist = []
        for node in path:
            innerlist.append([Node.objects.get(name=node).title, Node.objects.get(name=node).sep_url])
        outerlist.append(innerlist)
    return outerlist


def json_node_list(graph, source, target):
    """ Path MUST exist between source and target in graph """
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
    """ graph must only contain edges on nodes in node_list """
    output = []
    for edge in graph.edges:
        output.append(edge_to_indexed_dictionary(edge, node_list))
    return output
        

def edge_to_indexed_dictionary(edge: tuple, node_list: list):
    source_idx = list(filter(lambda x: x['name'] == edge[0], node_list))[0]['index']
    target_idx = list(filter(lambda x: x['name'] == edge[1], node_list))[0]['index']
    return {"source": source_idx, "target": target_idx}


def vega_dict(graph, source, target):
    """ graph should be a subgraph induced on source and target """
    nodes = json_node_list(graph, source, target)
    edges = json_edge_list(graph, nodes)
    vega_dict = {"nodes": nodes, "links": edges}
    vega_dict["directed"] = type(graph) == nx.classes.digraph.DiGraph
    return vega_dict


def vega_dict_from_full(source, target, is_undirected):
    nw = full_network.g if is_undirected else full_network.dg
    subgraph = directed_induced_subgraph(nw, source, target)
    return vega_dict(subgraph, source, target)
