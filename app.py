import base64
import numpy as np
from io import BytesIO
from flask import Flask, render_template, request
from networkx import from_edgelist, draw_networkx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx
app = Flask(__name__)

def plot_graph(edges, new_edges=None):
    G = nx.from_edgelist(edges)

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(1, 1, 1)

    pos = nx.spring_layout(G)

    # Draw the original graph
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_weight='bold', ax=ax)

    # Draw new_edges if provided, with red color
    if new_edges is not None:
        G.add_edges_from(new_edges)
        red_edges = [(u, v) for (u, v) in G.edges() if (u, v) in new_edges]
        nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', width=1, ax=ax)

    # Save the figure to a BytesIO object
    buf = BytesIO()
    canvas.print_png(buf)
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return img_str




@app.route('/', methods=['GET', 'POST'])
def index():
    graph_before_data = np.load('static/graph.npy')
    output_edges = np.load('static/output.npy')
    graph_before = plot_graph(graph_before_data)
    graph_after = None

    if request.method == 'POST':
        selected_edges = request.form.getlist('selected_edges')
        new_edges = [tuple(map(int, edge.split(','))) for edge in selected_edges]
        graph_after = plot_graph(graph_before_data, new_edges=new_edges)

    return render_template("index.html", graph_before_data=graph_before, graph_after_data=graph_after, output_edges=output_edges)

if __name__ == '__main__':
    app.run(port=4444,debug=True)
