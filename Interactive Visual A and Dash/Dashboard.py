import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px 
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
df.head()
print(df["Launch Site"].unique())

# Read the airline data into pandas dataframe
spacex_df = df
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40, "font-family":"Arial, Helvetica, sans-serif"}),
                                html.Div(["Input Component", dcc.Dropdown(id="site-dropdown", 
                                                                          options=[{"label":"All Sites","value":"ALL"},
                                                                                   {"label":"CCAFS LC-40","value":"CCAFS LC-40"},
                                                                                   {"label":"VAFB SLC-4E","value":"VAFB SLC-4E"},
                                                                                   {"label":"KSC LC-39A","value":"KSC LC-39A"},
                                                                                   {"label":"CCAFS SLC-40","value":"CCAFS SLC-40"}
                                                                                   ],
                                                                                   value="ALL",
                                                                                   placeholder="place holder here",
                                                                                   searchable=True
                                                                          )]),
                                html.Br(),

                            
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id="payload-slider", 
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0:"0", 100:"100"},
                                                value=[min_payload,max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ], style={"font-family":"Arial, Helvetica, sans-serif"})

@app.callback(Output(component_id="success-pie-chart", component_property="figure"),
              Input(component_id="site-dropdown", component_property="value"))

def get_pie_chart(entered_site):
    if entered_site=="ALL":
        fig=px.pie(spacex_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches for All Sites")
        
    else:
        filtered_df=spacex_df[spacex_df["Launch Site"]==entered_site]
        fig=px.pie(filtered_df,
                names="class",
                title=f"Total Success Launches for {entered_site}")

    return fig

@app.callback(
              Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id="payload-slider", component_property="value"),
              Input(component_id="site-dropdown", component_property="value"))

def get_scatter_plot(payload,entered_site):
    low,high=payload
    filtered_df=spacex_df[(spacex_df["Payload Mass (kg)"]>=low) &
                          (spacex_df["Payload Mass (kg)"]<=high)]
    if entered_site=="ALL":
        fig=px.scatter(filtered_df,
                       x="Payload Mass (kg)",
                       y="class",
                       color="Booster Version Category",
                       title="Correlation between Payload and Success for All Sites")
    else: 
        filtered_df=filtered_df[filtered_df["Launch Site"]==entered_site]
        fig=px.scatter(filtered_df,
                               x="Payload Mass (kg)",
                               y="class",
                               color="Booster Version Category",
                               title=f"Correlation between Payload and Success for {entered_site}")
    return fig 

        
if __name__ == '__main__':
    app.run(debug=True)