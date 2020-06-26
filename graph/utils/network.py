import pandas as pd
import networkx as nx


class Network:
    """
    graph_dict: A dictionary in the following format:
        { node1_name: {
            attribute1_key: value,
            attribute2_key: value,
            successor_nodes: [node1_name, node3_name],
            },
          node2_name: {
            attribute1_key: value,
            attribute2_key: value,
            successor_nodes: [node3_name],
            },
        }
    Node and attribute keys are hashables; values can be anything
    castable to a pandas 'object' type (but will be accessible as their
    original types in the self.dg and self.g attributes)
    'related_attribute': dictionary key for the list related nodes,
    which will be used to generate edges in the graph data structure. Each
    node must have a (possibly empty) list of related nodes.
    Instances have the following attributes:
        self.df - a Pandas dataframe representation of the graph
        self.dg - a networkx directed graph
        self.g - a networkx undirected graph
        self.dict - the dictionary passed at initialization
    """
    def __init__(self, graph_dict, related_attribute):
        Network.validate(graph_dict, related_attribute)
        self.dict = graph_dict
        self.df = pd.DataFrame.from_dict(graph_dict, orient='index')
        self.dg = Network.digraph(graph_dict, related_attribute)
        self.g = nx.Graph(self.dg)

    @staticmethod
    def validate(graph_dict, related_attribute):
        # Get sample value from first key
        sample_value = next(iter(graph_dict.items()))[1]
        for key, value in graph_dict.items():
            if value.keys() != sample_value.keys():
                raise ValueError("Attribute keys are inconsistent")
            if type(value[related_attribute]) != list:
                raise ValueError("Related attribute must be a list")
        return None

    @classmethod
    def from_jl(cls, filename, related_attribute):
        """Read crawled results file to dictionary"""
        with open(filename) as f:
            df = pd.read_json(f, lines=True, encoding='unicode-escape')
        pd_dict = df.to_dict(orient='index')
        raw = {}
        for key in pd_dict:
            node = pd_dict[key]["node"]
            raw[node] = pd_dict[key]
        return cls(raw, related_attribute)

    @staticmethod
    def digraph(graph_dict, related_attribute):
        dg = nx.DiGraph()
        # Add nodes and attributes
        
        for key, value in graph_dict.items():
            dg.add_node(key)
            for att_key, att_value in value.items():
                dg.nodes[key][att_key] = att_value
        # Add edges
        for key in graph_dict:
            for neighbor in graph_dict[key][related_attribute]:
                dg.add_edge(key, neighbor)
        return dg
