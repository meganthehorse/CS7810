##### Graph stuff
import os
import pandas as pd
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME

#  Directory Path Parameters
data_path = "./Dataset"
output_path = "./output"

# Prefixes
name_space = "http://semanticweb.org/soloflife/"
pfs = {
"solr": Namespace(f"{name_space}lod/resource/"),
"sol-ont": Namespace(f"{name_space}lod/ontology/"),
"dbo": Namespace("http://dbpedia.org/ontology/"),
"time": Namespace("http://www.w3.org/2006/time#"),
"ssn": Namespace("http://www.w3.org/ns/ssn/"),
"sosa": Namespace("http://www.w3.org/ns/sosa/"),
"provo": Namespace("http://www.w3.org/ns/prov#"),
"modl": Namespace("https://archive.org/services/purl/purl/modular_ontology_design_library"),
"cdt": Namespace("http://w3id.org/lindt/custom_datatypes#"),
"ex": Namespace("https://example.com/"),
"rdf": RDF,
"rdfs": RDFS,
"xsd": XSD,
"owl": OWL,
"time": TIME
}

# Initialization shortcut
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg

# rdf:type shortcut
a = pfs["rdf"]["type"] #isA prefix/relationship

# Initialize an empty graph
graph = init_kg()

# Initialize from a file
# filename = "path/to/file"
# with open(filename, "w") as f:
#     graph.parse(f)

#  Load in Asteroid_Distances.csv
asteroid_distances_path = os.path.join(data_path, "Asteroid_Distances.csv")
with open(asteroid_distances_path, "r") as inputF:
    lines = [line.strip() for line in inputF.readlines()]
    header = (lines[0].strip()).split(",")    

# for line in lines[1:]:
# lets just look at 1 asteroid...
for line in lines[1:2]:
    split = line.split(",")
    name = split[0]
    #  Mint the individual Asteroid
    asteroid_uri = pfs["solr"][f"Asteroid.{name}"] 
    #  Declare the Asteroid Concept to the SOL Ontology
    graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]) )
    graph.add( (asteroid_uri, a, pfs["sosa"]["FeatureOfInterest"]) )
    index = 1  # Index for header column
    for distances in split[1:]:
        monthyear = header[index]
        #  Mint the individual distance record per asteroid
        distance_record_uri = pfs["solr"][f"DistanceRecord.{name}.{monthyear}"]
        #  Declare the individual DR Concept to the SOL Ontology
        graph.add( (distance_record_uri, a, pfs["sol-ont"]["DistanceRecord"]) )
        #  Result->Quantity->QuantityKind (au)
        #                  ->QuantityValue (actual recording)
        #  Mint the Result and Quantity Nodes
        result_uri = pfs["solr"][f"Result.{name}.{monthyear}"]
        quantity_uri = pfs["modl"][f"Result.Quantity.{name}.{monthyear}"]
        quantity_kind_uri = pfs["modl"][f"Quantity.QuantityKind.{name}.{monthyear}"]
        quantity_value_uri = pfs["modl"][f"Quantity.QuantityValue.{name}.{monthyear}"]
        #  Declare the Result schema into the SOL Ontology      
        graph.add( () )        

        #  Mint the Time
        time_uri = pfs["solr"][f"time.{name}.{monthyear}"]
        #  Connect the Asteroid Concept to the DR Concept
        graph.add( (asteroid_uri, pfs["sol-ont"]["hasDistanceRecord"], distance_record_uri) )
        index+=1  #  next column



output_file = os.path.join(output_path, f"SOL_Asteroid.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
