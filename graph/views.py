import random
import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic, View

from networkx import read_gpickle
from networkx.exception import NetworkXNoPath

from dal import autocomplete

from graph.models import Node
from . import forms
from graph.utils import subgraph

# Create your views here.
# TODO: DRAW!
# TODO: 

PICKLE_PATH = 'sep_digraph_pickle'
NO_PATH_STRING = ("No path found! Here's your next paper title: "
                  '"The Surprising Ties between {} and {}"') 

def get_graph(path):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, path)
    graph = read_gpickle(filename)
    return graph

def index(request, *args):
    """Main page"""
    if request.GET != {}:
        print("here")
        # Assign node parameters
        q_head, q_tail = request.GET.get('h'), request.GET.get('t')
        head_node = get_object_or_404(Node, name=q_head)
        tail_node = get_object_or_404(Node, name=q_tail)
        # Check for subgraph
        try:
            graph = get_graph(PICKLE_PATH)
            subg = subgraph.induced_subgraph(graph, q_head, q_tail)
            paths = subgraph.all_shortest_paths(graph, q_head, q_tail)
            result_string = subgraph.result_string(graph, q_head, q_tail)
        except NetworkXNoPath: # No paths found!
            subg = None
            result_string = NO_PATH_STRING.format(head_node.title, tail_node.title)
            paths = []
    else:
        items = list(Node.objects.all())
        q_head, q_tail = random.sample(items, 2)
        subg = ''
        result_string = ''
        paths = []
    form = forms.NodeForm(initial={
        'h': q_head,
        't': q_tail,
    })
    print("Keys:")
    print(subg)
    return render(request, 'graph/index.html', {'form': form, 'result': result_string, 'subg': subg, 'paths': paths})

def result(request, *args):
    """Main page"""
    if request.GET != {}:
        print("here")
        # Assign node parameters
        q_head, q_tail = request.GET.get('h'), request.GET.get('t')
        head_node = get_object_or_404(Node, name=q_head)
        tail_node = get_object_or_404(Node, name=q_tail)
        # Check for subgraph
        try:
            graph = get_graph(PICKLE_PATH)
            subg = subgraph.induced_subgraph(graph, q_head, q_tail)
            paths = subgraph.all_shortest_paths(graph, q_head, q_tail)
            result_string = subgraph.result_string(graph, q_head, q_tail)
        except NetworkXNoPath: # No paths found!
            subg = None
            result_string = NO_PATH_STRING.format(head_node.title, tail_node.title)
            paths = []
    else:
        items = list(Node.objects.all())
        q_head, q_tail = random.sample(items, 2)
        subg = ''
        result_string = ''
        paths = []
    form = forms.NodeForm(initial={
        'h': q_head,
        't': q_tail,
    })
    print("Keys:")
    print(subg)
    return render(request, 'graph/result.html', {'form': form, 'result': result_string, 'subg': subg, 'paths': paths})
# class NodeSelectView(generic.FormView):
#     template_name = 'graph/node_form.html'
#     model = Node
#     form_class = forms.NodeForm
#     success_url = "/"

class NodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Node.objects.all()
        
        if self.q:
            qs = qs.filter(title__icontains=self.q) | qs.filter(name__icontains=self.q)
            
        return qs
    
    def get_result_label(self, item):
        return item.title

    def get_result_value(self, item):
        return item.name