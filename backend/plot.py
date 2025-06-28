import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import plotly.graph_objects as go

def check_layout():
    # Read prepared.json
    with open(r'H:\REPOSITORIES\music-viewer\frontend\public\prepared.json', 'r') as f:
        data = json.load(f)

    fig = go.Figure()

    for item in data:
        x = item['x']
        y = item['y']
        l = 100
        w = 100  # l/w = 100, so w = l/100 = 1
        fig.add_shape(
            type="rect",
            x0=x, y0=y,
            x1=x + l, y1=y + w,
            line=dict(color='red'),
            fillcolor=item['colour']
        )

    # Optionally, adjust limits to fit all boxes
    all_x = [item['x'] for item in data]
    all_y = [item['y'] for item in data]
    if all_x and all_y:
        fig.update_xaxes(range=[min(all_x) - 10, max(all_x) + l + 10])
        fig.update_yaxes(range=[min(all_y) - 10, max(all_y) + w + 10])

    fig.update_layout(
        title='All boxes with l/w=100',
        yaxis=dict(scaleanchor="x", scaleratio=1)
    )
    fig.show()