import json
import sqlite3
import plotly.graph_objects as go

from DashHtml import app

from dash.dependencies import Input, Output

from datetime import datetime

from Common import locationDataframe, locationDictionary, locationList
from Common import DATABASE_NAME, TABLE_NAME
from Common import mapbox_publictoken

# import string
def GetCashCount(vendor, location):
    cash_count_list = []
    
    # Connect to database.
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    for i in range(24):
        adjusted_hour = str(i) if int(i) > 9 else "0{0}".format(i)
        query = "SELECT SUM('total_amount') "+\
                "FROM '{0}' ".format(TABLE_NAME)+\
                "WHERE VendorID ='{0}'".format(str(vendor)) + " "
        if location != "*":
            query += "AND PULocationID = '{0}'".format(str(location)) + " "
        query += "AND tpep_pickup_datetime LIKE '%{0} {1}:%'".format("2017-04-02", adjusted_hour)
        # Debug print
        # print(query)
        cursor.execute(query)
        count = int(cursor.fetchone()[0])
        cash_count_list.append(count)

    return cash_count_list


def GetPassangerCount(vendor, location):
    passanger_count_list = []
    # Connect to database.
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    for i in range(24):
        adjusted_hour = str(i) if int(i) > 9 else "0{0}".format(i)
        query = "SELECT SUM('passanger_count') "+\
                "FROM '{0}' ".format(TABLE_NAME)+\
                "WHERE VendorID ='{0}'".format(str(vendor)) + " "
        if location != "*":
            query += "AND PULocationID = '{0}'".format(str(location)) + " "
        query += "AND tpep_pickup_datetime LIKE '%{0} {1}:%'".format("2017-04-02", adjusted_hour)
        # Debug print
        # print(query)
        cursor.execute(query)
        count = int(cursor.fetchone()[0])
        passanger_count_list.append(count)

    return passanger_count_list

def GetFigureCommon(xList, yList, text):
    return { 'data': [
            dict(
                x= xList[0], y= yList[0],
                text = text[0],
                mode='markers',
                marker={ 'size': 15, 'opacity': 0.8, 'line': {'width': 0.5, 'color': 'darkblue'} }
            ),
            dict(
                x= xList[1], y= yList[1],
                text = text[1],
                mode='markers',
                marker={ 'size': 15, 'opacity': 0.8, 'line': {'width': 0.5, 'color': 'gold'} }
            )
        ],
        'layout': dict( 
            xaxis={'title': text[2], },
            yaxis={'title': text[3], },
            hovermode='closest'
        )
    }

def GetFigureTotalCash(locationName, locationID):
    xList = []
    yList = []
    textList = []

    for i in range(1,3):
        xList.append(GetCashCount(i, locationID))
        yList.append(GetPassangerCount(i, locationID))
        textList.append("Vendor "+ str(i)+" in:" + locationName)    

    textList.append("# Of Passangers carried")
    textList.append("Total Money Gained")

    return GetFigureCommon(xList, yList, textList)

def GetFigurePassangerCount(locationName, locationID):
    xList = []
    yList = []
    textList = []
    for i in range(1,3):
        xList.append([j for j in range(24)])
        yList.append(GetPassangerCount(i, locationID))
        textList.append("Vendor "+ str(i)+" in:" + locationName)    

    textList.append("Hours")
    textList.append("# of Passangers carried")

    return GetFigureCommon(xList, yList, textList)

# CASH CHART
@app.callback(
    Output("passanger_cash_chart", "figure"),
    [Input("location_dropdown", "value")])
def update_graph(selectedLocation):
    if selectedLocation is 0 or selectedLocation is None:
        return GetFigureTotalCash("ALL REGIONS", "*")

    index = 0
    for i in range(locationDataframe.__len__()):
        if selectedLocation == locationDataframe['zone'][i]:
            index = i
            # print("index:"+ str(index))
            # print("selectedLocation:"+ str(selectedLocation))
            break

    return GetFigureTotalCash(selectedLocation, index)

# PASSANGER CHART
@app.callback(
    Output("passanger_chart", "figure"),
    [Input("location_dropdown", "value")])
def update_graph(selectedLocation):
    if selectedLocation is 0 or selectedLocation is None:
        return GetFigurePassangerCount("ALL REGIONS", "*")

    index = 0
    for i in range(locationDataframe.__len__()):
        if selectedLocation == locationDataframe['zone'][i]:
            index = i
            # print("index:"+ str(index))
            # print("selectedLocation:"+ str(selectedLocation))
            break

    return GetFigurePassangerCount(selectedLocation, index)
    
# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("taxi_map", "figure"),
    [Input("location_dropdown", "value")])
# def update_graph(datePicked, selectedData, selectedLocation):
def update_graph(selectedLocation):
    zoom = 8.0
    latInitial = 40.7273
    lonInitial = -73.9912

    if selectedLocation:
        zoom = 15.0
        latInitial = locationList[selectedLocation]["lat"]
        lonInitial = locationList[selectedLocation]["lon"]

    return go.Figure(
        data=[
            # Data for all rides based on date and time
            # Plot of important locations on the map
            go.Scattermapbox(
                lat=[locationList[i]["lat"] for i in locationList],
                lon=[locationList[i]["lon"] for i in locationList],
                mode="markers",
                hoverinfo="text",
                text=[i for i in locationList],
                marker=dict(size=8, color="#ffa0a0"),
            ),
        ],
        layout= go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken= mapbox_publictoken,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7273  # -73.9912
                style="dark",
                zoom=zoom,
            )
        )
    )

@app.callback( 
    Output('map_selected-data', 'children'),
    [Input('taxi_map', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent= 2)

@app.callback(
    Output('map_click-data', 'children'),
    [Input('taxi_map', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent= 2)

@app.callback(
    Output('hover-data', 'children'),
    [Input('passanger_chart', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('click-data', 'children'),
    [Input('passanger_chart', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@app.callback(
    Output('selected-data', 'children'),
    [Input('passanger_chart', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

@app.callback(
    Output('cash_hover-data', 'children'),
    [Input('passanger_cash_chart', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('cash_click-data', 'children'),
    [Input('passanger_cash_chart', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@app.callback(
    Output('cash_selected-data', 'children'),
    [Input('passanger_cash_chart', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

# @app.callback(
#     Output('map_relayout-data', 'children'),
#     [Input('date-picker', 'date'), Input('bar-selector','value')])
# def display_relayout_data(date, time):
#     connection = sqlite3.connect(DATABASE_NAME)
#     cursor = connection.cursor()

#     query = "SELECT COUNT('*') "+\
#             "FROM '{0}' ".format(TABLE_NAME)+\
#             "WHERE VendorID ='{0}'".format(str("*")) + " "
#     if date and date != None:
#         # date = datetime(2017,4,1)
#         query += "AND tpep_pickup_datetime LIKE '%{0} {1}:%'".format(date, time)
#     cursor.execute(query)
#     count = int(cursor.fetchone()[0])
        
#     return json.dumps(count, indent=2)

# @app.callback(
#     Output('map_relayout-data', 'children'),
#     [Input('passanger_chart', 'relayoutData')])
# def display_relayout_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)

if __name__ == '__main__':
    app.run_server(debug=True)