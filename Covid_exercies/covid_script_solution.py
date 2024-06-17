from pyqgis_scripting_ext.core import *

folder = "C:\\Users\\Lorenz\\Documents\\Advanced GIS\\"

geopackPath = "natural_earth_vector.gpkg\\packages\\"
geopackagePath = folder + geopackPath + "natural_earth_vector.gpkg"

provincesName = "ne_10m_admin_1_states_provinces"

HMap.remove_layers_by_name(["OpenStreetMap", provincesName])


outputFolder = folder + "output_covid\\"

provincesLayer = HVectorLayer.open(geopackagePath, provincesName)
provincesLayer.subset_filter("admin = 'Italy'")
HMap.add_layer(provincesLayer)


regionName2GeometryMap = {}
regionIndex = provincesLayer.field_index("region") 
for provinceFeature in provincesLayer.features():
    geometry = provinceFeature.geometry
    regionName = provinceFeature.attributes[regionIndex]
    
    regionGeometry = regionName2GeometryMap.get(regionName)
    if regionGeometry:
        regionGeometry = regionGeometry.union(geometry)
    else:
        regionGeometry = geometry
        
    regionName2GeometryMap[regionName] = regionGeometry
    
# for name, geom in regionName2GeometryMap.items():
#     print(name, geom.asWkt()[:30])
    
dataPath = folder + "data\\dpc-covid19-ita-regioni.csv"

with open(dataPath, "r") as file: #read the file
    lines = file.readlines()

day2featuresMap = {}
for index, line in enumerate(lines):
    line = line.strip()
    
    if index < 5000:
        lineSplit = line.split(",")
        #0 - date
        #3 - region
        #17 - total cases
        #4,5 - lat lon
        dayAndTime = lineSplit[0]
        dayAndTime = dayAndTime.split("T")
        day = dayAndTime[0]

        
        if day.endswith("01"):
            region = lineSplit[3]
            totalCases = int(lineSplit[17])
            
            lat = float(lineSplit[4])
            lon = float(lineSplit[5])
            dataPoint = HPoint(lon, lat)
            
            for regionName, regionGeometry in regionName2GeometryMap.items():
                if regionGeometry.intersects(dataPoint):
                    featuresList = day2featuresMap.get(day)
                    if featuresList:
                        featuresList.append((regionGeometry, [day, region, totalCases]))
                    else:
                        featuresList = [(regionGeometry, [day, region, totalCases])]
                    day2featuresMap[day] = featuresList
                    
                    
for day, featuresList in day2featuresMap.items():
    if day != "2020-04-01":
        continue
        
    print("Generating day", day)
    newLayerName = "covid_italy"
    HMap.remove_layers_by_name(newLayerName)
    
    schema = {
        "day": "string",
        "region": "string",
        "totcases": "int"
    }
    covidLayer = HVectorLayer.new(newLayerName, "MultiPolygon", "EPSG:4326", schema)
    
    for geometry, attributes in featuresList:
        covidLayer.add_feature(geometry, attributes)
        
    style = HFill("yellow") + HStroke("black", 0.5)
    
    covidLayer.set_style(style)
    HMap.add_layer(covidLayer)
    
    printer = HPrinter(iface)
    
    mapProperties = {
        "x": 5,
        "y": 25,
        "width": 285,
        "height": 180,
        "frame": True,
        "extent": provinceLayer.bbox()
    }
    
    printer.add_map(**mapProperties)
    
    legendProperties = {
        "x": 210,
        "y": 30,
        "width": 150,
        "height": 100,
        "frame": True
    }
    
    printer.add_legend(**legendProperties)
    
    labelProperties = {
        "x": 120,
        "y": 10,
        "text": "COVID Italy, total Casese",
        "bold": True
    }
    printer.add_label(**labelProperties)
    
    labelProperties = {
        "x": 30,
        "y": 190,
        "text": day,
        "font_size": 28,
        "bold": True
    }
    printer.add_label(**labelProperties)    


    ranges = [
        ["-inf", ]
    ]


    
    imageName = f"{day}_covid.png"
    
from PTL import Image
for path in imagePathList:
    img = IMage.open(path)
    imagesList.append(img)
    
    animationPath = f"{outputFolder}/covid_animation.gif"
    
    imagesList[0].save(animationPath)
    
    
    
