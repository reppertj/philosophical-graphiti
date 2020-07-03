import networkx as nx
from networkx.exception import NetworkXNoPath, NodeNotFound


def all_shortest_paths(graph: nx.Graph, source: str, target: str):
    """Returns generator; raises NetworkXNoPath if no path"""
    return nx.all_shortest_paths(graph, source, target)


def n_shortest_paths(graph: nx.Graph, source: str, target: str):
    """Returns number of shortest paths and degrees of separation"""
    try:
        paths = list(all_shortest_paths(graph, source, target))
        n_paths = len(paths)
        degrees = len(paths[0])
    except (NetworkXNoPath, NodeNotFound):
        n_paths, degrees = (0, 0)
    return n_paths, degrees


def result_string(graph: nx.Graph, source: str, target: str):
    if source == target:
        string = "Well, that was easy!"
    else:
        n_paths, degrees = n_shortest_paths(graph, source, target)
        path_word = "path" if n_paths == 1 else "paths"
        degree_word = "degree" if degrees == 2 else "degrees"
        string = f"Found {n_paths} {path_word} with {degrees - 1} {degree_word} of separation"    
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


def edges_on_paths(paths):
    return [(node, path[index + 1]) for path in paths for (index, node) in enumerate(path[:-1])]


def directed_induced_subgraph(graph, source:str, target: str):
    """
    Induced subgraph on edges along shortest paths between source
    and target. networkx.exception.NetworkXNoPath if no path
    """
    try:
        shortest_paths = all_shortest_paths(graph, source, target)
        edges = edges_on_paths(shortest_paths)
        subgraph = graph.edge_subgraph(edges)
    except NetworkXNoPath:
        raise
    if source == target:
        subgraph = nx.induced_subgraph(graph, source)
    return subgraph
