import numpy as np
import pandas as pd
import os
import secrets
from flask import Flask, render_template, request, session, send_file
import json
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def extract_n_hop_edges(output_edges, graph_edges):
    G = nx.Graph()
    G.add_edges_from(graph_edges)

    n_hop_nodes = set()
    for edge in output_edges:
        n_hop_nodes.update(list(nx.single_source_shortest_path_length(G, edge[0], cutoff=1).keys())[:5])
        n_hop_nodes.update(list(nx.single_source_shortest_path_length(G, edge[1], cutoff=1).keys())[:5])

    filtered_edges = []
    for edge in graph_edges:
        if edge[0] in n_hop_nodes and edge[1] in n_hop_nodes:
            filtered_edges.append(edge)
    return np.array(filtered_edges)

def load_raw_entities(file_path):
    raw_entities = {}
    with open(file_path, 'r') as f:
        for line in f:
            node_id, raw_name = line.strip().split('\t')
            raw_entities[int(node_id)] = raw_name
    return raw_entities

@app.route('/', methods=['GET', 'POST'])
def eal():
    graph_edges = np.load('static/graph.npy')
    output_edges = np.load('static/output.npy')[:2]
    graph_before_data = extract_n_hop_edges(output_edges, graph_edges)
    raw_entities_dbp = load_raw_entities('static/ea_dataset/dbp/entity_raw_rev.txt')
    raw_entities_wd = load_raw_entities('static/ea_dataset/wd/entity_raw_rev.txt')

    if request.method == 'POST':
        selected_edges = request.form.getlist('selected_edges')
        new_edges = [tuple(map(int, edge.split(','))) for edge in selected_edges]
        fixed_positions = session.get('fixed_positions', {})
        return render_template("index.html", graph_before_data=graph_before_data.tolist(), output_edges=output_edges.tolist(), new_edges=new_edges, fixed_positions=fixed_positions, raw_entities_dbp = raw_entities_dbp, raw_entities_wd = raw_entities_wd)

    G = nx.Graph()
    G.add_edges_from(graph_before_data)
    fixed_positions = {int(k): list(v) for k, v in nx.spring_layout(G, k=0.2, iterations=20).items()}
    session['fixed_positions'] = fixed_positions

    return render_template("index.html", graph_before_data=graph_before_data.tolist(), output_edges=output_edges.tolist(), new_edges=[], fixed_positions=fixed_positions, raw_entities_dbp = raw_entities_dbp, raw_entities_wd = raw_entities_wd)


if __name__ == '__main__':
    app.run(port=45011, debug=True)