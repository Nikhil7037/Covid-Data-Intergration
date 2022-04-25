import plotly.express as px
import pandas as pd

def create_worldGraph(df1):
    fig = px.choropleth(data_frame=df1,
                        locations="iso_alpha",
                        color="Confirmed",  # value in column 'Confirmed' determines color
                        hover_name="Country",
                        color_continuous_scale='Turbo',  # color scale red, yellow green
                        animation_frame="Date",
                        title = "Total Confirmed Cases")

    fig.show()

def create_DeltaWorldGraph(df1):
    fig = px.choropleth(data_frame=df1,
                        locations="iso_alpha",
                        color="DeltaConfirmed",  # value in column 'Confirmed' determines color
                        hover_name="Country",
                        color_continuous_scale='Turbo',  # color scale red, yellow green
                        animation_frame="Date",
                        title = "Delta Confirmed Cases")
    
    fig.show()

if __name__ == "__main__":
    kaggleHopkinsDataset = pd.read_csv("sourceIntegration.csv")
    create_worldGraph(kaggleHopkinsDataset)
    create_DeltaWorldGraph(kaggleHopkinsDataset)