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
        if item == region:
            regionsDict[region]: feature.geometry

fields = {
    "name": "String"
}

regionsLayer = HVectorLayer.new("regions", "Polygon", "EPSG:4326", fields)

for region, geo in regionsDict.items():
    regionsLayer.add_feature(geo, [region])


HMap.add_layer(regionsLayer)

