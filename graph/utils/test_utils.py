from django.test import TestCase

from graph.utils.network import Network
from graph.utils.subgraph import induced_subgraph

class NetworkTestCase(TestCase):
    def setUp(self):
        sep = Network.from_jl('related.jl', 'related')
        subg = induced_subgraph(subg, 'plato', 'husserl')

    def induced_subgraph_is_correct(self):
        """Correct subgraph is induced from source to target"""
        subg_nodes = str(subg.nodes)
        subg_edges = str(subg.edges)
        self.assertEqual(str(subg.nodes),
        "['time', 'lyotard', 'metaphysics', 'education-philosophy', 'categories', 'plato', 'husserl']")
        self.assertEqual(str(subg.edges), "[('time', 'husserl'), ('lyotard', 'husserl'), ('metaphysics', 'categories'), ('metaphysics', 'time'), ('education-philosophy', 'lyotard'), ('education-philosophy', 'plato'), ('categories', 'husserl'), ('categories', 'metaphysics'), ('plato', 'education-philosophy'), ('plato', 'metaphysics')]")