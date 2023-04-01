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
name_space = "http://soloflife.org/"
pfs = {
"solr": Namespace(f"{name_space}lod/resource/"),
"sol-ont": Namespace(f"{name_space}lod/ontology/"),
"sol-qk": Namespace(f"{name_space}lod/quantitykinds"),
"sol-unit": Namespace(f"{name_space}lod/units"),
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
"time": TIME,
"qudt": Namespace("http://qudt.org/schema/qudt/"),
}

# Initialization shortcut
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg

# rdf:type shortcut
a = pfs["rdf"]["type"] #isA prefix/relationship
hasNumericID = pfs["sol-ont"]["hasNumericID"]
hasCommonName = pfs["sol-ont"]["hasCommonName"]
hasDiscoveryName = pfs["sol-ont"]["hasDiscoveryName"]
# Initialize an empty graph
graph = init_kg()


asteroid_distances_path = os.path.join(data_path, "sbdb_query_results.csv")
with open(asteroid_distances_path, "r") as inputF:
    lines = [line.strip() for line in inputF.readlines()]
    header = (lines[0].strip()).split(",")    

# for line in lines[1:10]:
for line in lines[1:200000]:  # for each asteroid
    split = line.split(",")
    numericID = split[1].replace(" ", "_")
    asteroid_uri = pfs["solr"][f"Asteroid.{numericID}"]
    graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]) )


    split_fullName = split[0].split(" ")

    if(len(split_fullName) == 4):
        commonName = split_fullName[1]
        graph.add( (asteroid_uri, hasCommonName, Literal(commonName, datatype=XSD.string)) )

        discoveryName = str(split_fullName[2]) +" "+ str(split_fullName[3])
        discoveryName = discoveryName.replace("(", "")
        discoveryName = discoveryName.replace(")", "")
    elif(len(split_fullName) == 3):
        discoveryName = str(split_fullName[1]) +" "+ str(split_fullName[2])
        discoveryName = discoveryName.replace("(", "")
        discoveryName = discoveryName.replace(")", "")
    # if(len(split_fullName)<4 ):
    #     discoveryName = str(split_fullName[1]) +" "+ str(split_fullName[2])
    # else:    
    #  Mint the individual Asteroid
    graph.add( (asteroid_uri, hasNumericID, Literal(numericID, datatype=XSD.string)) )
    graph.add( (asteroid_uri, hasDiscoveryName, Literal(discoveryName, datatype=XSD.string)) )

output_file = os.path.join(output_path, f"SOL_Asteroid_Names.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
