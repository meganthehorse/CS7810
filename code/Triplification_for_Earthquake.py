##### Imports
# Python libraries
import os, json, pickle, sys
from datetime import datetime
# Geo stuff
import fiona
import shapely
from shapely import wkt
from shapely.geometry import Polygon, MultiPolygon, shape
import geopandas as gpd
# Graph stuff
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
# Earthquake dataset specific
import pandas as pd
import reverse_geocoder as rg
from util import add_geometry

##### Logging
def log(msg,tab_level=0):
    timestamp = datetime.now()
    tabs = "\t" * (tab_level+1)
    message = f"{timestamp}{tabs}{msg}"
    print(message)

##### Paths
# The directory hosting all raw data
data_path = "./data"
# The directory hosting the s2 cells
s2_path = "./s2_cells"
# The directory hosting admin regions
#admin_path = "./admin_regions"
# The directory hosting triples
output_path = "./output"

##### Graph stuff
# Prefixes
name_space = "http://stko-kwg.geog.ucsb.edu/"
pfs = {
"kwgr": Namespace(f"{name_space}lod/resource/"),
"kwg-ont": Namespace(f"{name_space}lod/ontology/"),
"geo": Namespace("http://www.opengis.net/ont/geosparql#"),
"geof": Namespace("http://www.opengis.net/def/function/geosparql/"),
"sf": Namespace("http://www.opengis.net/ont/sf#"),
"wd": Namespace("http://www.wikidata.org/entity/"),
"wdt": Namespace("http://www.wikidata.org/prop/direct/"),
"rdf": RDF,
"rdfs": RDFS,
"xsd": XSD,
"owl": OWL,
"time": TIME,
"dbo": Namespace("http://dbpedia.org/ontology/"),
"time": Namespace("http://www.w3.org/2006/time#"),
"ssn": Namespace("http://www.w3.org/ns/ssn/"),
"sosa": Namespace("http://www.w3.org/ns/sosa/"),
"cdt": Namespace("http://w3id.org/lindt/custom_datatypes#")
}
# Initialization shortcut
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg
# rdf:type shortcut
a = pfs["rdf"]["type"]

##### Load Data
log("Loading data.")
# Load all earthquake data into a pandas dataframe
earthquake_data_file = os.path.join(data_path, "earthquake_fulldata.csv")
earthquake_df = pd.read_csv(earthquake_data_file, header=0)
# Convert it into a geopandas dataframe
earthquake_gdf = gpd.GeoDataFrame(
    earthquake_df, geometry=gpd.points_from_xy(earthquake_df.longitude, earthquake_df.latitude))
# Columns used to create classes
eq_op_names = ['depth', 'mag', 'magType', 'nst', 'gap', 'dmin', 'rms', 'net', 'type',
          'horizontalError', 'depthError', 'magError', 'magNst', 'status','locationSource',
          'magSource']
log(f"Earthquake data loaded ({len(earthquake_gdf)} records).", 1)
# Loading the pickle file for s2 data for the contintental US
s2_file = os.path.join(s2_path, "S2_US_13_5070.pickle")
# with open(s2_file, "rb") as f:
#     # Open the pickle file
#     log("Loading the pickle file. This may take some time.", 1)    
#     s2_df = pickle.load(f)
#     s2_df.set_geometry("geometry", inplace=True)
#     log(f"crs='{s2_df.crs}'", 2)
#     log("Finished Loading the pickle file.", 1)
# Load the admin data
"""
# admin_file = os.path.join(admin_path, "admin_uris.tsv")
# admin_dict = dict()
admin_file = pd.read_csv("admin_uris.tsv",sep='\t')
# with open(admin_file) as admin_uris:
#     lines = admin_uris.readlines()
#     for line in lines:
#         cc, name, uri = line.strip().split("\t")
#         admin_dict[cc] = {"name": name, "uri": uri}
"""

##### Triplification
# Create our graph
graph = init_kg()
log("Starting triplification.")
log("Create earthquake observable properties.", 1)
eq_op_uris = dict()
for eq_op_name in eq_op_names:
    # Mint URI for the earthquake observable property
    eq_op_uri = pfs["kwgr"][f"EarthquakeObservableProperty.{eq_op_name}"]
    # Declare it
    # Add it to the observable properties list for convenience
    eq_op_uris[eq_op_name] = eq_op_uri
log("Triplify all earthquakes.", 1)
log(f"There are {len(earthquake_gdf)} records to triplify.", 2)
# Process each earthquake
prev = 0
count = 1
# for i in range(1001,1002,1000):
for i in range(10,11):
    for idx, row in earthquake_gdf[prev:i].iterrows():
        # Extract the earthquake id
        event_id = row['id']
        # Mint URI for the earthquake
        earthquake_uri = pfs["kwgr"][f"Earthquake.{event_id}"]
        log(earthquake_uri, 3)
        # Declare it
        graph.add( (earthquake_uri, a, pfs["kwg-ont"]["Earthquake"]) )
        ## Create the observation collection that will house all observations
        # Mint URI for the observation collection
        obs_col_uri = pfs["kwgr"][f"{'EarthquakeObservationCollection'}.{event_id}"]
        # Declare it
        graph.add( (obs_col_uri, a, pfs['kwg-ont']['EarthquakeObservationCollection']) )
        # Specify feature of interest
        graph.add( (obs_col_uri, pfs['sosa']["hasFeatureOfInterest"], earthquake_uri) ) 
        # Add the inverse
        graph.add( (earthquake_uri, pfs['sosa']["isFeatureOfInterestOf"], obs_col_uri) ) 
        # Specify the phenomenon time
        graph.add( (obs_col_uri, pfs['sosa']["phenomenonTime"], pfs["kwgr"][f"{'time'}.{event_id}"]) )
        ## Use the reverse geocoder to get the nearest city based on the earthquake coordinate
        # Expected Structure: https://pypi.org/project/reverse_geocoder/
        # Create the coordinate
        coordinate = (row['latitude'], row['longitude'])
        # Get the address from the reverse geocoder
        # This is a json object
        address = rg.get(coordinate, verbose=False)
        cc = address.get('cc')
        # if cc == "US":
        #     # Do S2 Integration
        #     row_df = earthquake_gdf[idx:idx+1]
        #     row_df = row_df.set_crs("epsg:4326")
        #     row_df = row_df.to_crs("epsg:5070")
        #     result = gpd.sjoin(row_df, s2_df, how="inner", op="within")
        #     print(result)
        #     log("encountered us eq")
        place = f"{address.get('name')}, {address.get('cc')}"
        eq_label = f"Earthquake near {place} at {row['time']}."
        graph.add( (earthquake_uri, RDFS['label'], Literal(eq_label)))
        ## Admin Integration
        try:
            pass
            #Get the URI from the 
            #admin_uri = admin_dict[cc]["uri"]
            # admin_uri = admin_file[cc]["uri"]
            # Turn it into an rdflib object
            # admin_uri = URIRef(admin_uri)
            # Add it to the graph
            # graph.add( (earthquake_uri, pfs["kwg-ont"]["sfWithin"], admin_uri) )
        except KeyError as e:
            log(f"Key Error in Admin Integration. Could not find: {cc}", 4)
        # Mint URI for the time
        time_uri = pfs["kwgr"][f"time.{event_id}"]
        # Declare it
        graph.add( (time_uri, a, pfs['time']['Instant']) )
        # Add the time triple
        graph.add( (time_uri, pfs['time']['inXSDDateTime'], Literal(row['time'], datatype = XSD.dateTime)) )
        ## Add geometry
        add_geometry(row["geometry"], earthquake_uri, graph, pfs["geo"]["hasGeometry"], pfs)
        ## Process the earthquake observable properties
        for eq_op_name in eq_op_names:
            # Mint URI for the observation
            eq_obs_uri = pfs["kwgr"][f"{'EarthquakeObservation'}.{event_id}.{eq_op_name}"]
            # Declare it
            graph.add( (eq_obs_uri, a, pfs["kwg-ont"]['EarthquakeObservation']) )
            # Connect it to the observation collection
            graph.add( (obs_col_uri, pfs['sosa']['hasMember'], eq_obs_uri) )
            # Specify the observable property
            graph.add( (eq_obs_uri, pfs['sosa']['observedProperty'], eq_op_uris[eq_op_name]) )
            # Specify the result of the observation
            if eq_op_name in ['dmin', 'gap']:
                graph.add( (eq_obs_uri, pfs['sosa']['hasSimpleResult'], Literal(row[eq_op_name], datatype=pfs["cdt"]["angle"])) )
            elif eq_op_name in ['rms']:
                graph.add( (eq_obs_uri, pfs['sosa']['hasSimpleResult'], Literal(row[eq_op_name], datatype=pfs["cdt"]["time"])) )
            elif eq_op_name in ['depthError', 'depth', 'horizontalError', 'magError', 'magNst', 'mag']:
                graph.add( (eq_obs_uri, pfs['sosa']['hasSimpleResult'], Literal(row[eq_op_name], datatype=pfs["cdt"]["ucum"])) )
            else:
                if eq_op_name == 'nst':
                    try:
                        res = int(row[eq_op_name]) 
                    except:
                        res = 0
                    graph.add( (eq_obs_uri, pfs['sosa']['hasSimpleResult'], Literal(res)) )
                else:
                    graph.add( (eq_obs_uri, pfs['sosa']['hasSimpleResult'], Literal(row[eq_op_name])) )
    ## Write triples intermittently to reduce memory footprint
    log(f"Progress: {idx} records triplified.", 2)
    log("Writing triples to file.", 3)
    output_file = os.path.join(output_path, f"earthquake-usgs-{count}.ttl")
    temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
    log(f"Finished writing triples (@ {output_file}).", 3)
    graph = init_kg()
    count += 1
    prev = i
    

log("Finished triplification.")
