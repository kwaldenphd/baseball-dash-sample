import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

########### Define your variables
# load schedule data from url
schedule = pd.read_csv("https://raw.githubusercontent.com/kwaldenphd/more-with-matplotlib/main/data/combined_nd_schedules_cleaned.csv")

# create datetime object from Standardized_Date field
schedule['Datetime'] = pd.to_datetime(schedule['Standardized_Date'])

# make new datatime column the index
schedule.set_index(['Datetime'], inplace=True)

githublink='https://github.com/kwaldenphd/football-structured-data/blob/main/background.md#football-schedules'
sourceurl='https://github.com/kwaldenphd/football-structured-data/blob/main/background.md#football-schedules'

########### Set up the chart


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
# setup dropdown for game type
type_dropdown = dcc.Dropdown(options=schedule['Game_Type'].unique(), value='Home')

# set colors/style
colors = {
    'background': '#0c2340',
    'text': '#c99700'
}

# setup layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, 
                      children=[
                                html.H1(
                                    children='Notre Dame Football Schedule Dashboard',
                                    style = {
                                        'textAlign': 'center',
                                        'color': colors['text'],
                                        'font': 'Arial'
                                    }),
                                html.Div([
                                          type_dropdown,
                                          dcc.Graph(id = 'schedule-points'),
                                          ])
                                ])

# set up callback for interactivity
@app.callback(
    Output(component_id = 'schedule-points', component_property='figure'), 
    Input(component_id = type_dropdown, component_property='value')
)

# setup function to generate plot
def update_graph(game_type):
  subset = schedule[schedule['Game_Type'] == game_type]
  bar_fig = px.bar(subset, x='Season', y='Pts', color_discrete_sequence=['#00843d'], title=f'Number of Points Over Time For {game_type}')
  return bar_fig

if __name__ == '__main__':
    app.run_server()
