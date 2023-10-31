import plotly.express as px

#Map drawing, receives dataframe as parameter
def draw_map(df):
    fig = px.scatter_mapbox(df, lon = df['LON'], lat = df['LAT'], zoom = 10, color = df['Color'] , size = df['Size'], width=900 , height=600 ,title='DIRECTIONS MAP')
    fig.update_layout(mapbox_style = "open-street-map")
    fig.update_layout(margin = {"r":0,"t":50,"l":0,"b":10})
    fig.show()
