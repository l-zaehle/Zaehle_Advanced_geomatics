from pyqgis_scripting_ext.core import *

folder = "C:\\Users\\Lorenz\\Documents\\Advanced GIS\\"

geopackPath = "natural_earth_vector.gpkg\\packages\\"
geopackagePath = folder + geopackPath + "natural_earth_vector.gpkg"

provincesName = "ne_10m_admin_1_states_provinces"

HMap.remove_layers_by_name(["OpenStreetMap", provincesName, "regions"])


# load open street map
osm = HMap.get_osm_layer()
HMap.add_layer(osm)

# load the province layer and create a subset with filter
provincesLayer = HVectorLayer.open(geopackagePath, provincesName)
HMap.add_layer(provincesLayer)

provincesLayer.subset_filter("admin = 'Italy'") #just show those features that are obeying to th filter


regionIndex = provincesLayer.field_index("region") 
provinceIndex = provincesLayer.field_index("name")

provinceFeatures = provincesLayer.features()

#create a list with all the regions of italy
regions = []
for feature in provinceFeatures:
    region = feature.attributes[regionIndex]
    if region not in regions:
        regions.append(region)
##print(regions)

#create a dictionary with the region as key and every single Province geometries as values
#Loop over the regions-list and check, if region is not yet in the dict, In this case a key (regionName) is set and the values are an empty list
#then all geometries for each key are being added to the values-list
regionsDict = {}
for item in regions:
    for feature in provinceFeatures:
        region = feature.attributes[regionIndex]
        if region not in regionsDict:
            regionsDict[region] = []
        if item == region:
            regionsDict[region].append(feature.geometry)

##print(regionsDict)
# creation of the regionsLayer
fields = {
    "name": "String"
}

regionsLayer = HVectorLayer.new("regions", "MultiPolygon", "EPSG:4326", fields)

#for loop accessing all elements in regionsDict
#region = key, PGeometries = values
for region, PGeometries in regionsDict.items():
    count = 0
    geo = PGeometries[-1]
    
    for i in range(len(PGeometries)):
        geo = geo.union(PGeometries[count])
        count +=1
    
    regionsLayer.add_feature(geo, [region])


HMap.add_layer(regionsLayer)


###-------------
#Adding the csv starts here
#-------------------

dataPath = folder + "data\\dpc-covid19-ita-regioni.csv"

with open(dataPath, "r") as file: #read the file'
    lines = file.readlines()

regionsFeatures = regionsLayer.features()
#workaround: only one day for now
date = "2020-02-24T18:00:00"

covidDict = {}

for line in lines[1:]: #skip headers
    if line.startswith("#") or len(line) == 0:
        continue
    line = line.strip().split(",")
    lat = float(line[4])
    lon = float(line[5])

    centerPoint = HPoint(lon,lat)

    if date == line[0]:
        for feature in regionsFeatures:
            if centerPoint.intersects(feature.geometry):
                covidDict[feature.attributes[0]] = line[6]
                
                
print(covidDict)


