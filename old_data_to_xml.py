import os
import sys
import pandas as pd

convert_direction = {1:"Northbound", 2: "Eastbound", 3: "Southbound", 4: "Westbound"}
convert_column = {"IncSerialNum" : "EventId",
"Description" : "LocationDescription", 
"Status" : "EventStatus", 
"Category" : "EventType",  
"InitDate" : "EventStartDate", 
"InitiatedBy" : "InitiatedBy",
"ResolveDate" : "EventEndDate", 
"ResolvedBy" : "ResolvedBy",
"RoadwayName" : "RoadwayName", 
"RoadwayType" : "RoadwayType",
"RoadwayDirection" : "Direction",
"DetectionMeans" : "DetectionMeans",
"Severity" : "LaneBlockageDescription", 
"Camera" : "Camera", 
"Weather" : "Weather",
"Temperature" : "Temperature",
"TrafficState" : "TrafficState",
"RoadSurface" : "RoadSurface", 
"LastUpdatedBy" : "LastUpdatedBy",
"IncTimeStamp" : "LastUpdate",
"URCPTEA" :  "URCPTEA",
"URCPTEB" : "URCPTEB",
"WorkOrderNumber" : "WorkOrderNumber",
"FireZone" : "FireZone"}


def update_roaddirect(key):
    return convert_direction.get(key, "")


def convert_to_xml(row):
    xml = ["<Event>"]
    for field in row.index:
        xml.append('    <{0}>{1}</{2}>'.format(field, row[field], field))
    xml.append("</Event>")
    return '\n'.join(xml)

def main():
    road_events = pd.DataFrame.from_csv("./MassDOThack/Road_Events/Road_Events.csv")
    road_events["RoadwayDirection"] = road_events["RoadwayDirection"].apply(update_roaddirect)
    road_events.rename(columns=convert_column, inplace=True)
    out = '<ERS_Events xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n    <UpdateDate>2014-11-04T21:58:50.850815-05:00</UpdateDate>\n    <Events>'
    out += '\n'.join(road_events.apply(convert_to_xml, axis=1))
    out += "    </Events>\n</ERS_Events>"
    with open("converted.xml", "w") as outfile:
        outfile.write(out)




if __name__ == '__main__':
    main()