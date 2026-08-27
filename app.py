import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load dataset with updated URL
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
df = pd.read_csv(URL)
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month_name()

# Initialize Dash App
app = dash.Dash(__name__)

# TASK 2.1: Add title to the dashboard
# TASK 2.2: Add RadioItems and Dropdown
# TASK 2.3: Add empty divisions for output
app.layout = html.Div(children=[
    html.H1(
        "Australia Wildfire Dashboard", 
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}
    ),
    
    html.Div([
        # TASK 2.2: Radio items for Region
        html.Div([
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems(
                id='region-radio',
                options=[{'label': r, 'value': r} for r in df['Region'].unique()],
                value='NSW',
                inline=True
            )
        ]),
        
        # TASK 2.2: Dropdown for Year
        html.Div([
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
                value=2005
            )
        ])
    ]),
    
    # TASK 2.3: Output divisions
    html.Div([
        html.Div([], id='plot1'),
        html.Div([], id='plot2')
    ], style={'display': 'flex'})
])

# TASK 2.4: Callback decorator
@app.callback(
    [Output(component_id='plot1', component_property='children'),
     Output(component_id='plot2', component_property='children')],
    [Input(component_id='region-radio', component_property='value'),
     Input(component_id='year-dropdown', component_property='value')]
)
# TASK 2.5: Callback function
def update_graph(input_region, input_year):
    region_year_df = df[(df['Region'] == input_region) & (df['Year'] == int(input_year))]
    
    # Chart 1: Pie Chart
    est_data = region_year_df.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(
        est_data, 
        values='Estimated_fire_area', 
        names='Month', 
        title=f"{input_region} : Monthly Average Estimated Fire Area in {input_year}"
    )
    
    # Chart 2: Bar Chart
    veg_data = region_year_df.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(
        veg_data, 
        x='Month', 
        y='Count', 
        title=f"{input_region} : Monthly Average Count of Presumed Vegetation Fires in {input_year}"
    )
    
    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

if __name__ == '__main__':
    app.run(port=8050, host='0.0.0.0', debug=True)