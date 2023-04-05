import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from networkx import from_edgelist, draw_networkx 
import matplotlib
matplotlib.use('Agg')  # Add this line before importing pyplot
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)
 
def plot_graph(edges):
    G = from_edgelist(edges)
    plt.figure()
    # Replace the draw function with draw_networkx
    draw_networkx(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_weight='bold')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')


@app.route('/', methods=['GET', 'POST'])
def index():
    graph_before_data = np.load('static/graph.npy')
    output_edges = np.load('static/output.npy')

    if request.method == 'POST':
        selected_edges = request.form.getlist('selected_edges')
        selected_edges = [tuple(map(int, edge.split(','))) for edge in selected_edges]
        graph_after_data = np.concatenate((graph_before_data, selected_edges), axis=0)
    else:
        graph_after_data = None

    graph_before = plot_graph(graph_before_data)
    graph_after = plot_graph(graph_after_data) if graph_after_data is not None else None

    return render_template("index.html", graph_before_data=graph_before, graph_after_data=graph_after, output_edges=output_edges)

if __name__ == "__main__":
    app.run(port=3336, debug=True)
