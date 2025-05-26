import plotly.graph_objects as go

# 仮のデータ
models = ["Model A", "Model B", "Model C"]
min_vals = [1.5, 2.0, 1.0]  # 能力の最小値（kWなど）
max_vals = [5.0, 4.0, 6.0]  # 能力の最大値

# 横棒用に、startとwidthを作る
start_vals = min_vals
widths = [max_vals[i] - min_vals[i] for i in range(len(min_vals))]

fig = go.Figure()

for i, model in enumerate(models):
    fig.add_trace(go.Bar(
        x=[widths[i]],
        y=[model],
        base=start_vals[i],
        orientation='h',
        name=model,
        hovertemplate=f"{model}: {min_vals[i]}～{max_vals[i]} kW<extra></extra>"
    ))

fig.update_layout(
    title="エアコン機種ごとの能力範囲（kW）",
    xaxis_title="能力（kW）",
    barmode='stack',  # 'stack' にすると見やすくなる場合も
    bargap=0.3,
    template='plotly_white'
)

fig.show()