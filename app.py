import numpy as np
import os
import secrets
from flask import Flask, render_template, request, session
import json
import networkx as nx

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_before_data = np.load('static/graph.npy')
    output_edges = np.load('static/output.npy')

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
    app.run(port=4480, debug=True)
