import random

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import generic, View
from django.db.models.functions import Lower, Length

from django_user_agents.utils import get_user_agent

from networkx.exception import NetworkXNoPath

from dal import autocomplete

from graph.models import Node, full_network
from . import forms
from graph.utils import render_subgraph
from graph.utils.neighbors import render_neighborhood


def index(request):
    items = list(Node.objects.all())
    q_head, q_tail = random.sample(items, 2)
    q_neighbors = random.choice(items)
    form = forms.NodeForm(initial={
        'h': q_head,
        't': q_tail,
    })
    neighborform = forms.CenterForm(initial={
        'c': q_neighbors,
    })
    return render(request, 'graph/index.html', {'form': form, 'neighborform': neighborform})


def result(request):
    q_head = request.GET.get('h')
    q_tail = request.GET.get('t')
    is_undirected = True if request.GET.get('u') == "true" else False
    head_title = get_object_or_404(Node, name=q_head).title
    tail_title = get_object_or_404(Node, name=q_tail).title
    form = forms.NodeForm(initial={
        'h': q_head,
        't': q_tail,
        })
    sentence, paths, render_vega, json_data_path = (render_subgraph.
                                                    results(q_head, q_tail, is_undirected))
    return render(request, 'graph/result.html',
                  {'form': form, 'sentence': sentence, 'paths': paths,
                   'render_vega': render_vega, 'json_data_path':
                   json_data_path, 'q_head': q_head, 'q_tail': q_tail,
                   'is_undirected': is_undirected, 'head_title': head_title,
                   'tail_title': tail_title, 'random': False})


def get_random(request):
    items = list(Node.objects.all())
    head, tail = random.sample(items, 2)
    q_head, head_title = head.name, head.title
    q_tail, tail_title = tail.name, tail.title
    form = forms.NodeForm(initial={
        'h': q_head,
        't': q_tail,
        })
    is_undirected = False
    sentence, paths, render_vega, json_data_path = (render_subgraph.
                                                    results(q_head, q_tail, is_undirected))
    return render(request, 'graph/result.html',
                  {'form': form, 'sentence': sentence, 'paths': paths,
                   'render_vega': render_vega, 'json_data_path':
                   json_data_path, 'q_head': q_head, 'q_tail': q_tail,
                   'is_undirected': is_undirected, 'head_title': head_title,
                   'tail_title': tail_title, 'random': True})

def vega_spec(request, source=None, directed_value='dg', target=None):
    json_data_path = f"{source}_sub{directed_value}data_{target}.json"
    return render(request, 'graph/vega_graph_spec.json', {'json_data_path': json_data_path})


def subgraph_json(request, source=None, directed_value='dg', target=None):
    get_object_or_404(Node, name=source)
    get_object_or_404(Node, name=target)
    is_undirected = True if directed_value == 'g' else False
    json_dict = render_subgraph.vega_dict_from_full(source, target, is_undirected)
    return JsonResponse(json_dict, json_dumps_params={'ensure_ascii': False})


def neighbors(request):
    center_req = request.GET.get('c')
    try:
        center_obj = Node.objects.get(name=center_req)
    except Node.DoesNotExist:
        center_obj = random.choice(list(Node.objects.all()))
    center_name = center_obj.name
    center_title = center_obj.title
    center_url = center_obj.sep_url
    form = forms.CenterForm(initial={
        'c': center_name
         })
    json_nodes, json_edges, sentence, node_dicts = render_neighborhood(center_name)
    return render(request, 'graph/neighbors.html', context={
        "center_title": center_title,
        "center_name": center_name,
        "center_url": center_url,
        "json_nodes": json_nodes,
        "json_edges": json_edges,
        "sentence": sentence,
        "form": form,
        "render_vega": True,
        "nodes": node_dicts
    })



def more(request):
    return render(request, 'graph/more.html')


class NodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Node.objects.all()
        
        if self.q:
            qs = qs.filter(title__icontains=self.q).order_by(Lower('title'))
            
        return qs
    
    def get_result_label(self, item):
        return item.title

    def get_result_value(self, item):
        return item.name