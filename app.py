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
print(data.info())

# %%
# Sample data dictionary (you can replace this with your own)
data_dictionary = {
    'Index': 'Unique identifying number',
    'Publishing Year': 'The year that the book was published in', 
    'Title': 'The name of the book',
    'Author': 'The author of the book',
    'Author Rating': 'The rating for an author based on their previous work',
    'Book Average Rating': 'The average of the rating given by readers',
    'Book Ratings Count': 'The amount of ratings a book has',
    'Genre': 'The genre the book belongs to',
    'Gross Sales': 'The total sales revenue generated per book',
    'Publisher Revenue': 'The total revenue the publisher gains by the books sales',
    'Sale Price': 'The price the book is sold at',
    'Sales Rank': 'The books rank based on its sales perfromance compared within its category (genre)',
    'Publisher': 'The company that published the book',
    'Units Sold': 'Count of books sold per title'}

# %%
sales_by_publisher = data.groupby('Publisher')['Gross Sales'].sum().reset_index()


# %%
stylesheets = ['/Users/yasminazizi/Desktop/DS 4003/bootstrap.css'] # Load the css stylesheet


app = Dash(__name__, external_stylesheets=stylesheets) 
server = app.server

# layout
app.layout = html.Div([
   html.Div([
        html.H1('Books Dashboard', style={'display': 'inline-block',  'padding': '10px'}),
        html.Img(src="/Users/yasminazizi/Desktop/DS 4003/books.png", style={'height': '30px', 'margin-right': '10px'}),
    ]),

    html.Div([
        html.P('This dashboard explores trends in top selling books. Picking a book can be lengthy and difficult due to the large selection and limited tools to make desicions. Depending on what perspective is taken this dataset can be used to lead reading choices or inventory selection amongst other purposes. A bookestore owner can use this data to enhance sales and manage inventory. A novice reader can use this information to guide where to start.'),
    ]),

    html.Div([

        html.H2('Data Dictionary', style={'textAlign': 'center', 'color': 'black'}),
        html.Div([
        dcc.Dropdown(
            id='variable-dropdown',
            options=[{'label': var, 'value': var} for var in data_dictionary.keys()],
            value=list(data_dictionary.keys())[0]  # Set default value
        ),
        ]),
        html.Div(id='variable-definition-output')

    ], style = {'backgroundColor': '#D2B48C'} ),

    html.Div(style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'padding': '10px'}, children=[
        html.H2("Top Ten Books by Units Sold", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='datatable',
            columns=[
                {'name': 'Title', 'id': 'Title'},
                {'name': 'Units Sold', 'id': 'Units Sold'}
            ],
            data=data.nlargest(10, 'Units Sold')[['Title', 'Units Sold']].to_dict('records'),  # Get top 10 books by gross sales
            style_table={'overflowX': 'scroll'},
            style_cell={'textAlign': 'left'},
        )
    ]),

    html.Div(style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'padding': '10px'}, children=[
        html.H2("Top Ten Books by Gross Sales", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='datatable1',
            columns=[
                {'name': 'Title', 'id': 'Title'},
                {'name': 'Gross Sales', 'id': 'Gross Sales'}
            ],
            data=data.nlargest(10, 'Gross Sales')[['Title', 'Gross Sales']].to_dict('records'),  # Get top 10 books by gross sales
            style_table={'overflowX': 'scroll'},
            style_cell={'textAlign': 'left'},
        )
    ]),

    html.Div(style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'padding': '10px'}, children=[
        html.H2("Top Ten Books by Avg. Rating", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='datatable2',
            columns=[
                {'name': 'Title', 'id': 'Title'},
                {'name': 'Book Average Rating', 'id': 'Book Average Rating'}
            ],
            data=data.nlargest(10, 'Book Average Rating')[['Title', 'Book Average Rating']].to_dict('records'),  # Get top 10 books by gross sales
            style_table={'overflowX': 'scroll'},
            style_cell={'textAlign': 'left'},
        )
    ]),

   html.Div([
        html.H2('Gross Sales by Publisher', style={'textAlign': 'center', 'color': 'black'}),
        html.P('This bar chart displays the total amount of sales each publisher featured in the data set has accumulated.', style={'textAlign': 'center', 'color': 'black'}),
        dcc.Checklist(
            id='publisher-checkboxes',
            options=[{'label': publisher, 'value': publisher} for publisher in sales_by_publisher['Publisher'].unique()],
            value=[sales_by_publisher['Publisher'].unique()[0]],  # Set default value to the first publisher
            labelStyle={'display': 'in-line', 'margin-bottom': '5px'}  # Display checkboxes vertically
        ),
        dcc.Graph(id='sales-bar-chart'),
    ]),

    html.Div([
        html.H2("Book Sales v. Book Rating", style={'textAlign': 'center', 'color': 'black'}), # Create header   
        html.P("This data analyzes Book Sales based on a book's ratings.", style={'textAlign': 'center', 'color': 'black'}), # align text and make font black
    
        # dropdown for the author name
        dcc.Dropdown( 
            id='Publisher',
            multi=True,
            options=[{"label": x, "value": x} for x in sorted(data['Publisher'].unique())],
            value=[data['Publisher'].unique()[0]],
            className='six columns'
        ),  
         dcc.RangeSlider(
             id='year-slider',
             min=data['Publishing Year'].min(),
             max= data['Publishing Year'].max(),
             value=[data['Publishing Year'].min(), data['Publishing Year'].max()],
             marks={str(year): str(year) if year % 50 == 0 else '' for year in data['Publishing Year'].unique()},
             step=100,
             tooltip={'always_visible': True},
             className='six columns'
         )
     ], className='row', style={'padding': 10}),
    
     dcc.Graph(id='graph', figure=px.scatter(data, x='Book Average Rating', y='Gross Sales', title='Book Rating v. Book Sales')), # Plotly Express graph
 ], style={'padding': 20, }) 
 

# Define callback to update variable definition output
@app.callback(
    Output('variable-definition-output', 'children'),
    [Input('variable-dropdown', 'value')]
)
def update_output(selected_variable):
    if selected_variable is not None:
        definition = data_dictionary.get(selected_variable, 'Definition not found')
        return html.Div([
            #html.H3(selected_variable),
            html.P(definition)
        ])
    else:
        return "Select a variable"
    
@app.callback(
    Output('graph', 'figure'),
    [Input('Publisher', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(pub_values, year_range):
    filtered_data = data[
        (data['Publisher'].isin(pub_values)) &
        (data['Publishing Year'] >= year_range[0]) &
        (data['Publishing Year'] <= year_range[1])
    ]
    fig = px.scatter(filtered_data, x='Book Average Rating', y='Gross Sales', title='Book Rating v. Book Sales',
                     hover_data={'Title': True, 'Gross Sales': True, 'Author': True},  # Add hover information
                     #trendline='ols',  # Add trendline using ordinary least squares regression
                     color='Publisher',  # Use color to represent genre
                     labels={'Book Average Rating': 'Average Rating', 'Gross Sales': 'Sales'},  # Customize axis labels
                     )
    fig.update_layout(
        xaxis_title='Average Rating',  # Add x-axis title
        yaxis_title='Gross Sales',  # Add y-axis title
        hovermode='closest',  # Display hover information for closest data point
        dragmode='lasso',  # Allow users to select data points with lasso tool
        showlegend=True,  # Show legend
        legend_title='Publisher',  # Customize legend title
    )
    return fig

@app.callback(
    Output('sales-bar-chart', 'figure'),
    [Input('publisher-checkboxes', 'value')]
)
def update_bar_chart(selected_publishers):
    filtered_sales_by_publisher = sales_by_publisher[sales_by_publisher['Publisher'].isin(selected_publishers)]
    fig = px.bar(filtered_sales_by_publisher, x='Publisher', y='Gross Sales', title='Gross Sales by Publisher',
                 hover_data={'Publisher': True, 'Gross Sales': True},  # Add hover information
                 color='Gross Sales',  # Use color to represent indexed gross sales
                 color_continuous_scale='Blues',  # Choose a color scale
                 labels={'Gross Sales': 'Indexed Gross Sales'},  # Customize axis labels
                 )
    fig.update_layout(
        xaxis_title='Publisher',  # Add x-axis title
        yaxis_title='Total Gross Sales',  # Add y-axis title
        hovermode='closest',  # Display hover information for closest data point
        showlegend=True,  # Show legend
        legend_title='Gross Sales',  # Customize legend title
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



