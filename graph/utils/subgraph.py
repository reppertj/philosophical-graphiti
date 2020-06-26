import networkx as nx
from networkx.exception import NetworkXNoPath

from graph.utils.network import Network


def all_shortest_paths(graph: nx.Graph, source: str, target: str):
    """Returns generator; raises NetworkXNoPath if no path"""
    return nx.all_shortest_paths(graph, source, target)


def n_shortest_paths(graph: nx.Graph, source: str, target: str):
    """Returns number of shortest paths and degrees of separation"""
    try:
        paths = list(all_shortest_paths(graph, source, target))
        n_paths = len(paths)
        degrees = len(paths[0])
    except NetworkXNoPath:
        n_paths, degrees = (0, 0)
    return n_paths, degrees


def result_string(graph: nx.Graph, source: str, target: str):
    result = n_shortest_paths(graph, source, target)
    string = "Found {} paths with {} degrees of separation.".format(*result)
    if source == target:
        string = "Well, that was easy!"
    return string


def nbunch_of_shortest_paths(graph, source, target):
    """
    List of nodes in all shortest paths between source and target
    Raises networkx.exception.NetworkXNoPath if no path
    """
    paths = all_shortest_paths(graph, source, target)
    try:
        nbunch = [node for path in paths for node in path]
    except NetworkXNoPath:
        raise
    return nbunch


def induced_subgraph(graph, source: str, target: str):
    """
    Induced subgraph on nodes on shortest paths between source and target
    Raises networkx.exception.NetworkXNoPath if no path
    """
    try:
        nbunch = nbunch_of_shortest_paths(graph, source, target)
    except NetworkXNoPath:
        raise
    return graph.subgraph(nbunch)
