from network import Network
import networkx as nx


sep = network_graph('related.jl', method='json_lines')


def all_shortest_paths(graph: nx.Graph, source: str, target: str):
    """Returns generator; raises NetworkXNoPath if no path"""
    return nx.all_shortest_paths(graph, source, target)


def nbunch_of_shortest_paths(graph, source, target):
    paths = all_shortest_paths(graph, source, target)
    nbunch = [node for path in paths for node in path]
    return nbunch


def induced_subgraph(graph, source: str, target: str):
    nbunch = nbunch_of_shortest_paths(graph, source, target)
    return nx.induced_subgraph(graph, nbunch).copy()


# TODO: Add exception handling for NetworkXNoPath
def sample_subgraph():
    subg = induced_subgraph(sep.dg, 'plato', 'husserl')
    return subg
