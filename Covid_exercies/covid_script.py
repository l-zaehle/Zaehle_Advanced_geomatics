from pyqgis_scripting_ext.core import *

folder = "C:\\Users\\Lorenz\\Documents\\Advanced GIS\\"

geopackPath = "natural_earth_vector.gpkg\\packages\\"
geopackagePath = folder + geopackPath + "natural_earth_vector.gpkg"

provincesName = "ne_10m_admin_1_states_provinces"

HMap.remove_layers_by_name(["OpenStreetMap", provincesName, "regions"])


provincesLayer = HVectorLayer.open(geopackagePath, provincesName)

# load open street m titels layer
osm = HMap.get_osm_layer()
HMap.add_layer(osm)

HMap.add_layer(provincesLayer)

provincesLayer.subset_filter("admin = 'Italy'") #just show those features that are obeying to th filter


regionIndex = provincesLayer.field_index("region") 
provinceIndex = provincesLayer.field_index("name")

regionsFeatures = provincesLayer.features()
regions = []
regionsDict = {}

for feature in regionsFeatures:
    region = feature.attributes[regionIndex]
    if region not in regions:
        regions.append(region)


for item in regions:
    for feature in regionsFeatures:
        region = feature.attributes[regionIndex]
        if region not in regionsDict:
            regionsDict[region] = []
        if item == region:
            regionsDict[region].append(feature.geometry)

print(regionsDict)
"""
fields = {
    "name": "String"
}

regionsLayer = HVectorLayer.new("regions", "Polygon", "EPSG:4326", fields)

for region, PGeometries in regionsDict.items():
    count = 0
    geo = PGeometries[-1]
    for i in range(len(PGeometries)):
        geo = geo.merge(PGeometries[count])
        count =+1
        
    regionsLayer.add_feature(geo, [region])


HMap.add_layer(regionsLayer)
"""
