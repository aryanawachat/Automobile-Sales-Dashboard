#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024)]
# Create the layout of the app
app.layout = html.Div([

    # Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 24
        }
    ),

    # Report Type Dropdown
    dcc.Dropdown(
        id='dropdown-statistics',
        options=dropdown_options,
        placeholder='Select a report type',
        value='Select Statistics',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),

    # Year Dropdown
    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select-year',
        value='Select-year',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),

    # Output Container
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex'}
        )
    ])

])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True
#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):

    # Recession Statistics
    if selected_statistics == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        # Plot 1
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales during Recession'
            )
        )

        # Plot 2
        average_sales = recession_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Automobile Sales by Vehicle Type during Recession'
            )
        )

        # Plot 3
        exp_rec = recession_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertisement Expenditure Share by Vehicle Type during Recession'
            )
        )

        # Plot 4
        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div([
                html.Div([R_chart1], style={'width': '50%'}),
                html.Div([R_chart2], style={'width': '50%'})
            ], style={'display': 'flex'}),

            html.Div([
                html.Div([R_chart3], style={'width': '50%'}),
                html.Div([R_chart4], style={'width': '50%'})
            ], style={'display': 'flex'})
        ]

    # Yearly Statistics
    elif selected_statistics == 'Yearly Statistics' and input_year:

        yearly_data = data[data['Year'] == input_year]

        # Plot 1
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Average Automobile Sales'
            )
        )

        # Plot 2
        mas = yearly_data.groupby(
            'Month'
        )['Automobile_Sales'].sum().reset_index()

        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        # Plot 3
        avr_vdata = yearly_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year)
            )
        )

        # Plot 4
        exp_data = yearly_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure by Vehicle Type'
            )
        )

        return [
            html.Div([
                html.Div([Y_chart1], style={'width': '50%'}),
                html.Div([Y_chart2], style={'width': '50%'})
            ], style={'display': 'flex'}),

            html.Div([
                html.Div([Y_chart3], style={'width': '50%'}),
                html.Div([Y_chart4], style={'width': '50%'})
            ], style={'display': 'flex'})
        ]

    return []
# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)

