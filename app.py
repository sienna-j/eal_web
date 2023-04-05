import numpy as np
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_before_data = np.load('static/graph.npy')
    output_edges = np.load('static/output.npy')

    if request.method == 'POST':
        selected_edges = request.form.getlist('selected_edges')
        new_edges = [tuple(map(int, edge.split(','))) for edge in selected_edges]
        return render_template("index.html", graph_before_data=graph_before_data.tolist(), output_edges=output_edges.tolist(), new_edges=new_edges)

    return render_template("index.html", graph_before_data=graph_before_data.tolist(), output_edges=output_edges.tolist(), new_edges=[])

if __name__ == '__main__':
    app.run(port=4449, debug=True)
