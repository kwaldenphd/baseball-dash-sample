import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

##### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Baseball Team Explorer"

##### Load Data and Setup Layout
# load data
teams = pd.read_csv("https://raw.githubusercontent.com/kwaldenphd/baseball-dash-sample/main/team-total-time.csv")

# set list of colors
color = [px.colors.qualitative.Bold[0], px.colors.qualitative.Bold[1], px.colors.qualitative.Bold[2], px.colors.qualitative.Bold[3], px.colors.qualitative.Bold[4], px.colors.qualitative.Bold[5], px.colors.qualitative.Bold[6], px.colors.qualitative.Bold[7], px.colors.qualitative.Bold[10]]

# setup dropdown for game type
type_dropdown = dcc.Dropdown(options= teams['affiliation'].sort_values(ascending=True).unique(), value='STL')

# setup layout
app.layout = html.Div(
    html.Div(
        children = [
            html.H1("Explore Number of Major and Minor League Teams by Franchise Over Time"),
            html.Label('Choose Franchise: '),
            type_dropdown,
            dcc.Graph(id = 'teams'),
            html.A('Data Source', href="baseball-reference.com/"),
            html.Br(),
            html.A('Data File', href="https://github.com/kwaldenphd/baseball-dash-sample/blob/main/team-total-time.csv"),
            html.Br(),
            html.A('Code on GitHub', href="https://github.com/kwaldenphd/baseball-dash-sample"),
        ]))

# set up callback for interactivity
@app.callback(
    Output(component_id = 'teams', component_property='figure'), 
    Input(component_id = type_dropdown, component_property='value')
)

# setup function to generate plot
def update_graph(affiliation):
  subset = teams[teams['affiliation'] == affiliation]
  fig = px.bar(subset, x='season', y = 'number', color='level', 
               category_orders = {'level': ['MLB', 'AAA', 'AA', 'A+', 'A', 'A-', 'Rk', 'FRk', 'Other']}, 
               labels = {'affiliation': 'Major League Franchise', 'number': 'Number of Teams', 'season':'Season', 'level': 'Level'}, 
               hover_name = 'level', title= 'Number of Major and Minor League Teams By Franchise', 
               color_discrete_sequence=color)
  fig.update_yaxes(title = 'Total Number of Teams')
  return fig

##### run app
if __name__ == '__main__':
    app.run_server(debug=True)
