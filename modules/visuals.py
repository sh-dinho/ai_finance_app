import plotly.graph_objects as go

def radar_chart_subscores(subscores: dict):
    categories = list(subscores.keys())
    values = list(subscores.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Financial FIS'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False
    )
    return fig