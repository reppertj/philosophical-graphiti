import os

from django.db import models

from graph.utils.network import Network

GRAPH_JL_PATH = "utils/related.jsonl"
RELATED_NODE_KEY = "related"

# One time initialization of full_network object for use globally
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, GRAPH_JL_PATH)
full_network = Network.from_jl(filename, RELATED_NODE_KEY)


# Create your models here.
class Node(models.Model):
    '''
    For convenience and display only; not used for network analysis
    and not the authoritative source. Must be migrated from the Network object,
    which is read from a serialized file (currently .jl) and kept in memory
    '''
    name = models.CharField(max_length=80, primary_key=True)
    title = models.CharField(max_length=200)
    sep_url = models.URLField()
    pub_date = models.DateField(null=True)
    rev_date = models.DateField(null=True)
    
    # class Meta:
    #     ordering = ['title']


'''
Edges are not currently supported in database; they are kept in memory in a Network object
'''
# class Edge(models.Model):
#     head = models.ForeignKey(Node, on_delete=models.PROTECT,
#                              related_name="edge_head")
#     tail = models.ForeignKey(Node, on_delete=models.PROTECT,
#                              related_name="edge_tail")