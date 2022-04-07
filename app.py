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
app.title = "#NotreDameWillChangeYouIfYouLetIt"

##### Load Data and Setup Layout
# load schedule data from url
schedule = pd.read_csv("https://raw.githubusercontent.com/kwaldenphd/more-with-matplotlib/main/data/combined_nd_schedules_cleaned.csv")

# create datetime object from Standardized_Date field
schedule['Datetime'] = pd.to_datetime(schedule['Standardized_Date'])

# make new datatime column the index
schedule.set_index(['Datetime'], inplace=True)

# subset data for games after 1938
subset = schedule[schedule['Season'] >= 1938)]

# set colors/style
colors = {
    'background': '#0c2340',
    'text': '#c99700',
    'green': '#00843d'
}

# setup dropdown for game type
type_dropdown = dcc.Dropdown(options=subset['Game_Type'].unique(), value='Home')

# setup layout
app.layout = html.Div(
    html.Div(
        children = [
            html.H1("Explore Notre Dame Football Schedules", style={'color':colors['background'], 'font':'Arial'}),
            html.Label('Choose Game Type:'),
            type_dropdown,
            dcc.Graph(id = 'schedule-points'),
            html.A('Code on GitHub', href="https://github.com/kwaldenphd/sample-dash-app", style={'color':colors['text']}),
            html.Br(),
            html.A('Data Source', href="https://github.com/kwaldenphd/football-structured-data/blob/main/background.md#football-schedules", style={'color':colors['text']})
        ]))

# set up callback for interactivity
@app.callback(
    Output(component_id = 'schedule-points', component_property='figure'), 
    Input(component_id = type_dropdown, component_property='value')
)

# setup function to generate plot
def update_graph(game_type):
  subset2 = subset[subset['Game_Type'] == game_type]
  bar_fig = px.bar(subset2, x='Season', y='Pts', color='Conf', title=f'Number of Points Over Time For {game_type} Games', hover_name = 'Standardized_Date', hover_data=['Standardized_Opponent'])
  return bar_fig

##### run app
if __name__ == '__main__':
    app.run_server(debug=True)
