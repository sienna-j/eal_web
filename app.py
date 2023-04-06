import numpy as np
import os
import secrets
from flask import Flask, render_template, request, session
import json
import networkx as nx

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def two_hop_edges(output_edges, graph_edges):
    G = nx.Graph()
    G.add_edges_from(graph_edges)

    two_hop_nodes = set()
    for edge in output_edges:
        two_hop_nodes.update(nx.single_source_shortest_path_length(G, edge[0], cutoff=3).keys())
        two_hop_nodes.update(nx.single_source_shortest_path_length(G, edge[1], cutoff=3).keys())

    filtered_edges = []
    for edge in graph_edges:
        if edge[0] in two_hop_nodes and edge[1] in two_hop_nodes:
            filtered_edges.append(edge)
    return np.array(filtered_edges)

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_edges = np.load('static/graph.npy')
    output_edges = np.load('static/output.npy')
    graph_before_data = two_hop_edges(output_edges, graph_edges)

    if request.method == 'POST':
        selected_edges = request.form.getlist('selected_edges')
        new_edges = [tuple(map(int, edge.split(','))) for edge in selected_edges]
        fixed_positions = session.get('fixed_positions', {})
        return render_template("index.html", graph_before_data=graph_before_data.tolist(), output_edges=output_edges.tolist(), new_edges=new_edges, fixed_positions=fixed_positions)

    G = nx.Graph()
    G.add_edges_from(graph_before_data)
    fixed_positions = {int(k): list(v) for k, v in nx.spring_layout(G).items()}
    session['fixed_positions'] = fixed_positions

    return render_template("index.html", graph_before_data=graph_before_data.tolist(), output_edges=output_edges.tolist(), new_edges=[], fixed_positions=fixed_positions)

if __name__ == '__main__':
    app.run(port=45554, debug=True)
