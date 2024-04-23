# %% [markdown]
# # Sprint 4 Books Dashboard
# ## Yasmin Azizi 
# ## DS 4003

# %%
#import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dash_table, dcc, html, Input, Output, State 
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


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
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/Users/yasminazizi/Desktop/DS 4003/bootstrap.css'])
server = app.server

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# Define the layout of the application
app.layout = html.Div([
    # Header section
   
    html.Div([
         html.H1('Books Dashboard', style={'display': 'inline-block',  'padding': '10px'}),
         html.Img(src="https://img.freepik.com/premium-vector/book-logo-template-design-education-icon-sign-symbol_752732-614.jpg", style={'height': '40px', 'margin-right': '20px'}),
    ]),

    html.Div([
        html.Div(style={'position': 'absolute', 'top': '10px', 'right': '10px'}, children=[
        html.A(html.Button('GitHub', style={'margin-right': '10px'}), href='http://github.com/ya9nf/Books-Dash', target='_blank'),
         ]),
     ]),

    # Description section
    html.Div([
        html.P('This dashboard explores trends in top selling books. Picking a book can be lengthy and difficult due to the large selection and limited tools to make desicions. Depending on what perspective is taken this dataset can be used to lead reading choices or inventory selection amongst other purposes. A bookestore owner can use this data to enhance sales and manage inventory. A novice reader can use this information to guide where to start.'),
    ], style={'padding': '20px', 'backgroundColor': '#bdc3c7', 'borderRadius': '5px', 'color': '#333'}),

    # Data dictionary section
    html.Div([
        html.H2('Data Dictionary', style={'textAlign': 'center', 'color': '#2c3e50'}),
        dcc.Dropdown(
            id='variable-dropdown',
            options=[{'label': var, 'value': var} for var in data_dictionary.keys()],
            value=list(data_dictionary.keys())[0],
            style={'width': '50%', 'margin': '10px auto', 'color': '#34495e'},
        ),
        html.Div(id='variable-definition-output', style={'textAlign': 'center', 'color': '#7f8c8d'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'margin': '20px 0', 'borderRadius': '5px'}),

    # Sections for data tables
    html.Div([
        # Top ten books by Units Sold
        html.Div([
            html.H2("Top Ten Books by Units Sold", style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='datatable',
                columns=[{'name': 'Title', 'id': 'Title'}, {'name': 'Units Sold', 'id': 'Units Sold'}],
                data=data.nlargest(10, 'Units Sold')[['Title', 'Units Sold']].to_dict('records'),
                style_table={'overflowX': 'scroll'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#3498db', 'color': 'white'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#ecf0f1'}
                ]
            )
        ], style={'width': '30%', 'padding': '10px', 'backgroundColor': '#95a5a6', 'margin': '10px', 'borderRadius': '5px'}),

        # Top ten books by Gross Sales
        html.Div([
            html.H2("Top Ten Books by Gross Sales", style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='datatable1',
                columns=[{'name': 'Title', 'id': 'Title'}, {'name': 'Gross Sales', 'id': 'Gross Sales'}],
                data=data.nlargest(10, 'Gross Sales')[['Title', 'Gross Sales']].to_dict('records'),
                style_table={'overflowX': 'scroll'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#3498db', 'color': 'white'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#ecf0f1'}
                ]
            )
        ], style={'width': '30%', 'padding': '10px', 'backgroundColor': '#95a5a6', 'margin': '10px', 'borderRadius': '5px'}),

        # Top ten books by Avg. Rating
        html.Div([
            html.H2("Top Ten Books by Avg. Rating", style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='datatable2',
                columns=[{'name': 'Title', 'id': 'Title'}, {'name': 'Book Average Rating', 'id': 'Book Average Rating'}],
                data=data.nlargest(10, 'Book Average Rating')[['Title', 'Book Average Rating']].to_dict('records'),
                style_table={'overflowX': 'scroll'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#3498db', 'color': 'white'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#ecf0f1'}
                ]
            )
        ], style={'width': '30%', 'padding': '10px', 'backgroundColor': '#95a5a6', 'margin': '10px', 'borderRadius': '5px'}),

    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    # Additional charts section
    html.Div([
        # Gross Sales by Publisher
        html.Div([
            html.H2('Gross Sales by Publisher', style={'textAlign': 'center'}),
            html.P('This bar chart displays the total amount of sales each publisher featured in the data set has accumulated.', style={'textAlign': 'center'}),
            dcc.Checklist(
                id='publisher-checkboxes',
                options=[{'label': publisher, 'value': publisher} for publisher in sales_by_publisher['Publisher'].unique()],
                value=[sales_by_publisher['Publisher'].unique()[0]],  # Set default value to the first publisher
                labelStyle={'display': 'inline', 'margin': '5px'}  # Display checkboxes inline
            ),
            dcc.Graph(id='sales-bar-chart'),
        ], style={'width': '50%', 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),

        # Book Sales v. Book Rating
        html.Div([
            html.H2("Book Sales v. Book Rating", style={'textAlign': 'center'}),
            html.P("This data analyzes book sales compared to its ratings.", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='Publisher',
                multi=True,
                options=[{"label": x, "value": x} for x in sorted(data['Publisher'].unique())],
                value=[data['Publisher'].unique()[0]],
            ),
            dcc.RangeSlider(
                id='year-slider',
                min=data['Publishing Year'].min(),
                max=data['Publishing Year'].max(),
                value=[data['Publishing Year'].min(), data['Publishing Year'].max()],
                marks={str(year): str(year) for year in range(data['Publishing Year'].min(), data['Publishing Year'].max()+100, 1000)},
                tooltip={'always_visible': True},
            ),
            dcc.Graph(id='graph')
        ], style={'width': '50%', 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'}),

], style={'padding': '20px'})


# Define callback to update the text output in the Data Dictionary section
@app.callback(
    Output('variable-definition-output', 'children'),
    [Input('variable-dropdown', 'value')]
)
def update_output(selected_variable):
    if selected_variable is not None:
        definition = data_dictionary.get(selected_variable, 'Definition not found')
        return html.Div([
            html.P(definition, style={'padding': '10px', 'backgroundColor': '#ecf0f1', 'borderRadius': '5px', 'color': '#2c3e50'})
        ])
    else:
        return html.P("Select a variable from the dropdown", style={'color': '#e74c3c'})

# Define callback to update the graph based on publisher selection and year range
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
    fig = px.scatter(
        filtered_data, 
        x='Book Average Rating', 
        y='Gross Sales', 
        title='Book Rating vs. Book Sales',
        color='Publisher', 
        labels={'Book Average Rating': 'Average Rating', 'Gross Sales': 'Sales'}
    )
    fig.update_layout(
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#ecf0f1',
        font_color='#34495e',
        title_font_color='#2c3e50',
        legend_title_font_color='#2c3e50',
        legend_bgcolor='#bdc3c7',
        xaxis_title='Average Rating',
        yaxis_title='Gross Sales',
        showlegend=True
    )
    return fig

# Define callback to update the bar chart for sales by publisher
@app.callback(
    Output('sales-bar-chart', 'figure'),
    [Input('publisher-checkboxes', 'value')]
)
def update_bar_chart(selected_publishers):
    filtered_sales_by_publisher = sales_by_publisher[sales_by_publisher['Publisher'].isin(selected_publishers)]
    fig = px.bar(
        filtered_sales_by_publisher, 
        x='Publisher', 
        y='Gross Sales', 
        title='Gross Sales by Publisher',
        color='Gross Sales',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#ecf0f1',
        font_color='#34495e',
        title_font_color='#2c3e50',
        xaxis_title='Publisher',
        yaxis_title='Total Gross Sales',
        showlegend=False
    )
    return fig




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



