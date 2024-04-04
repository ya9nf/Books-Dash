# %% [markdown]
# # Sprint 4 Books Dashboard
# ## Yasmin Azizi 
# ## DS 4003

# %%
#import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dash_table, dcc, html, Input, Output, State # update to import


# %%
data = pd.read_csv('data.csv')

# %%
print(data.info)

# %%
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Load the css stylesheet

graph1 = Dash(__name__, external_stylesheets=stylesheets) 
server = graph1.server

# layout
graph1.layout = html.Div([
    html.H1("Book Sales v. Book Rating", style={'textAlign': 'center', 'color': 'black'}), # Create header
    
    html.P("This data analyzes Book Sales based on a book's ratings.", style={'textAlign': 'center', 'color': 'black'}), # align text and make font black
    
    html.Div([
        # dropdown for the author name
        dcc.Dropdown( 
            id='Author',
            multi=True,
            options=[{"label": x, "value": x} for x in sorted(data['Author'].unique())],
            value=[data['Author'].unique()[0]],
            className='six columns'
        ),  
        # dropdown for the book name
        dcc.Dropdown( 
            id='Book Name',
            multi=True,
            options=[{"label": x, "value": x} for x in sorted(data['Book Name'].unique())],
            value=[data['Book Name'].unique()[0]],
            className='six columns'
        ),  
        # range slider for the publiidhing year 
        dcc.RangeSlider(
            id='year-slider',
            min=data['Publishing Year'].min(),
            max=data['Publishing Year'].max(),
            value=[data['Publishing Year'].min(), data['Publishing Year'].max()],
            marks={str(year): str(year) if year % 100 == 0 else '' for year in data['Publishing Year'].unique()},
            step=None,
            tooltip={'always_visible': True},
            className='six columns'
        )
    ], className='row', style={'padding': 10}),
    
    dcc.Graph(id='graph', figure=px.scatter(data, x='Book_average_rating', y='gross sales', title='Book Rating v. Book Sales')), # Plotly Express graph
], style={'padding': 20})

# call back for drowndown and range sliders
@graph1.callback(
    Output('graph', 'figure'),
    [Input('Author', 'value'),
     Input('Book Name', 'value'),
     Input('year-slider', 'value')])
def update_graph(author_values, book_values, year_range):
    filtered_data = data[
        (data['Author'].isin(author_values)) &
        (data['Book Name'].isin(book_values)) &
        (data['Publishing Year'] >= year_range[0]) &
        (data['Publishing Year'] <= year_range[1])
    ]
    
    fig = px.scatter(filtered_data, x='Book_average_rating', y='gross sales', title='Book Rating v. Book Sales')
    return fig

# run the app
if __name__ == '__main__':
    graph1.run_server(debug=True)

# I am struggling deciding if this filter / UI elements will control the entirre dashboard or just the graph, 
#I am also sturggling to find unique stylesheets, 
# and also implementing BCE years for the range slider (they apear as negative)


