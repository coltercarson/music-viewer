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

def plot_island_circles(radii, centres):
    import plotly.graph_objects as go

    fig = go.Figure()

    for r, c in zip(radii, centres):
        x0, y0 = c[0] - r, c[1] - r
        x1, y1 = c[0] + r, c[1] + r
        fig.add_shape(
            type="circle",
            x0=x0, y0=y0,
            x1=x1, y1=y1,
            line=dict(color='blue'),
            fillcolor='rgba(0,0,255,0.2)'
        )

    # Optionally, adjust limits to fit all circles
    if centres and radii:
        xs = [c[0] for c in centres]
        ys = [c[1] for c in centres]
        min_x = min(x - r for x, r in zip(xs, radii))
        max_x = max(x + r for x, r in zip(xs, radii))
        min_y = min(y - r for y, r in zip(ys, radii))
        max_y = max(y + r for y, r in zip(ys, radii))
        fig.update_xaxes(range=[min_x - 10, max_x + 10])
        fig.update_yaxes(range=[min_y - 10, max_y + 10])

    fig.update_layout(
        title='Island Circles',
        yaxis=dict(scaleanchor="x", scaleratio=1)
    )
    fig.show()