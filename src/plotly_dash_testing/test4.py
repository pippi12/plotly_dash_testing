import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import pandas as pd

# 仮データ
models = ["Model A", "Model B", "Model C"]
# 冷房
cool_min = [1.5, 2.0, 1.0]
cool_max = [5.0, 4.0, 6.0]
# 暖房
heat_min = [1.2, 1.8, 0.9]
heat_max = [4.5, 3.8, 5.5]
# 効率
cool_eff = [6.1, 5.8, 6.5]
heat_eff = [4.2, 4.5, 4.0]
# 騒音
cool_noise = [45, 48, 42]
heat_noise = [43, 46, 40]
# 能力とCOP
capacity_data = {
    "Model A": [4.0, 4.5, 5.0, 5.5, 6.0],
    "Model B": [3.5, 3.8, 4.0, 4.2, 4.5],
    "Model C": [5.0, 5.5, 6.0, 6.5, 7.0],
}
cop_data = {
    "Model A": [3.2, 3.4, 3.5, 3.6, 3.7],
    "Model B": [3.6, 3.7, 3.8, 3.9, 4.0],
    "Model C": [3.0, 3.1, 3.2, 3.3, 3.4],
}
colors = {"Model A": "green", "Model B": "blue", "Model C": "orange"}

# # 冷房時能力範囲（横棒）
# cool_bar = go.Figure()
# for i, model in enumerate(models):
#     cool_bar.add_trace(go.Bar(
#         x=[cool_max[i] - cool_min[i]],
#         y=[model],
#         base=cool_min[i],
#         orientation='h',
#         name=model,
#         hovertemplate=f"{model}: {cool_min[i]}～{cool_max[i]} kW<extra></extra>"
#     ))
# cool_bar.update_layout(
#     title="冷房時能力範囲",
#     xaxis_title="能力（kW）",
#     barmode='stack',
#     height=300,
#     margin=dict(l=40, r=10, t=40, b=40)
# )

# # 暖房時能力範囲（横棒）
# heat_bar = go.Figure()
# for i, model in enumerate(models):
#     heat_bar.add_trace(go.Bar(
#         x=[heat_max[i] - heat_min[i]],
#         y=[model],
#         base=heat_min[i],
#         orientation='h',
#         name=model,
#         hovertemplate=f"{model}: {heat_min[i]}～{heat_max[i]} kW<extra></extra>"
#     ))
# heat_bar.update_layout(
#     title="暖房時能力範囲",
#     xaxis_title="能力（kW）",
#     barmode='stack',
#     height=300,
#     margin=dict(l=40, r=10, t=40, b=40)
# )

# # 効率（縦棒）
# eff_bar = go.Figure()
# eff_bar.add_trace(go.Bar(
#     x=models, y=cool_eff, name="冷房期間効率", marker_color='skyblue'
# ))
# eff_bar.add_trace(go.Bar(
#     x=models, y=heat_eff, name="暖房期間効率", marker_color='orange'
# ))
# eff_bar.update_layout(
#     title="期間効率",
#     yaxis_title="効率",
#     barmode='group',
#     height=300,
#     margin=dict(l=40, r=10, t=40, b=40)
# )

# # 騒音（縦棒）
# noise_bar = go.Figure()
# noise_bar.add_trace(go.Bar(
#     x=models, y=cool_noise, name="冷房最大能力時", marker_color='deepskyblue'
# ))
# noise_bar.add_trace(go.Bar(
#     x=models, y=heat_noise, name="暖房最大能力時", marker_color='tomato'
# ))
# noise_bar.update_layout(
#     title="最大能力時騒音値",
#     yaxis_title="騒音値（dB）",
#     barmode='group',
#     height=300,
#     margin=dict(l=40, r=10, t=40, b=40)
# )

# # 能力とCOP（散布図）
# scatter = go.Figure()
# colors = {"Model A": "green", "Model B": "blue", "Model C": "orange"}

# for model in models:
#     scatter.add_trace(go.Scatter(
#         x=capacity_data[model],
#         y=cop_data[model],
#         mode='markers+text',
#         text=[model]*len(capacity_data[model]),
#         textposition='top center',
#         marker=dict(size=15, color=colors[model]),
#         name=model
#     ))

# # scatter.add_trace(go.Scatter(
# #     x=capacity, y=cop, mode='markers+text', text=models,
# #     textposition='top center', marker=dict(size=15, color='green')
# # ))
# scatter.update_layout(
#     title="能力とCOPの関係",
#     xaxis_title="能力（kW）",
#     yaxis_title="COP",
#     height=400,
#     margin=dict(l=40, r=10, t=40, b=40)
# )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id="model-dropdown",
                options=[{"label": m, "value": m} for m in models],
                value=models,  # デフォルトで全選択
                multi=True,
                placeholder="機種を選択"
            ),
            width=12,
            style={"margin": "16px"}
        )
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="cool-bar"), width=3),
        dbc.Col(dcc.Graph(id="eff-bar"), width=3),
        dbc.Col(dcc.Graph(id="noise-bar"), width=3),
    ], style={"height": "50vh"}),
    dbc.Row([
        dbc.Col(dcc.Graph(id="heat-bar"), width=3),
        dbc.Col(dcc.Graph(id="scatter"), width=6),
    ], style={"height": "50vh"}),
], fluid=True)

@app.callback(
    Output("cool-bar", "figure"),
    Output("heat-bar", "figure"),
    Output("eff-bar", "figure"),
    Output("noise-bar", "figure"),
    Output("scatter", "figure"),
    [Input("model-dropdown", "value")]
)
def update_graphs(selected_models):
    # インデックス取得
    idx = [models.index(m) for m in selected_models if m in models]

    # 冷房時能力範囲
    cool_bar = go.Figure()
    for i in idx:
        cool_bar.add_trace(go.Bar(
            x=[cool_max[i] - cool_min[i]],
            y=[models[i]],
            base=cool_min[i],
            orientation='h',
            name=models[i],
            hovertemplate=f"{models[i]}: {cool_min[i]}～{cool_max[i]} kW<extra></extra>"
        ))
    cool_bar.update_layout(
        title="冷房時能力範囲",
        xaxis_title="能力（kW）",
        barmode='stack',
        height=300,
        margin=dict(l=40, r=10, t=40, b=40)
    )

    # 暖房時能力範囲
    heat_bar = go.Figure()
    for i in idx:
        heat_bar.add_trace(go.Bar(
            x=[heat_max[i] - heat_min[i]],
            y=[models[i]],
            base=heat_min[i],
            orientation='h',
            name=models[i],
            hovertemplate=f"{models[i]}: {heat_min[i]}～{heat_max[i]} kW<extra></extra>"
        ))
    heat_bar.update_layout(
        title="暖房時能力範囲",
        xaxis_title="能力（kW）",
        barmode='stack',
        height=300,
        margin=dict(l=40, r=10, t=40, b=40)
    )

    # 効率
    eff_bar = go.Figure()
    eff_bar.add_trace(go.Bar(
        x=[models[i] for i in idx], y=[cool_eff[i] for i in idx], name="冷房期間効率", marker_color='skyblue'
    ))
    eff_bar.add_trace(go.Bar(
        x=[models[i] for i in idx], y=[heat_eff[i] for i in idx], name="暖房期間効率", marker_color='orange'
    ))
    eff_bar.update_layout(
        title="期間効率",
        yaxis_title="効率",
        barmode='group',
        height=300,
        margin=dict(l=40, r=10, t=40, b=40)
    )

    # 騒音
    noise_bar = go.Figure()
    noise_bar.add_trace(go.Bar(
        x=[models[i] for i in idx], y=[cool_noise[i] for i in idx], name="冷房最大能力時", marker_color='deepskyblue'
    ))
    noise_bar.add_trace(go.Bar(
        x=[models[i] for i in idx], y=[heat_noise[i] for i in idx], name="暖房最大能力時", marker_color='tomato'
    ))
    noise_bar.update_layout(
        title="最大能力時騒音値",
        yaxis_title="騒音値（dB）",
        barmode='group',
        height=300,
        margin=dict(l=40, r=10, t=40, b=40)
    )

    # 散布図
    scatter = go.Figure()
    for i in idx:
        m = models[i]
        scatter.add_trace(go.Scatter(
            x=capacity_data[m],
            y=cop_data[m],
            mode='markers',
            text=["冷房Aなどの試験条件を表示可能"]*len(capacity_data[m]),
            textposition='top center',
            marker=dict(size=15, color=colors[m]),
            name=m
        ))
    scatter.update_layout(
        title="能力とCOPの関係",
        xaxis_title="能力（kW）",
        yaxis_title="COP",
        height=400,
        margin=dict(l=40, r=10, t=40, b=40)
    )

    return cool_bar, heat_bar, eff_bar, noise_bar, scatter

if __name__ == "__main__":
    app.run_server(debug=True, port=1234)