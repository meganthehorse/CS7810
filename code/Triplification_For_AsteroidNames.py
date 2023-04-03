##### Graph stuff
import os
import pandas as pd
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME

#  Directory Path Parameters
data_path = "./Dataset"
output_path = "./output"
FILE_COUNT = 25 # the higher the value, the more files but smaller

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

# rdf:type shortcut
a = pfs["rdf"]["type"] #isA prefix/relationship
hasNumericID = pfs["sol-ont"]["hasNumericID"]
hasCommonName = pfs["sol-ont"]["hasCommonName"]
hasDiscoveryName = pfs["sol-ont"]["hasDiscoveryName"]

# Initialization shortcut
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg

def triple_names():
    asteroid_distances_path = os.path.join(data_path, "asteroid_name_reference.csv")
    with open(asteroid_distances_path, "r") as inputF:
        lines = [line.strip() for line in inputF.readlines()]
        header = (lines[0].strip()).split(",")    

    start = 1
    next = 1
    iter = int(len(lines)/FILE_COUNT)
    for i in range(FILE_COUNT):
        # Initialize an empty graph
        graph = init_kg()
        start = next
        count=0
        for row in range(start, (start+iter)):  # for each asteroid
            if(row == len(lines)):
                break
            line = lines[row]
            split = line.split(",")
            numericID = split[3]
            discoveryName = split[0]
            #  Mint Asteroid
            asteroid_uri = pfs["solr"][f"Asteroid.{discoveryName.replace(' ','_')}"]
            graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]) )
            if(split[4] != ""):  #  Add Common Name when available
                commonName = split[4]
                graph.add( (asteroid_uri, hasCommonName, Literal(commonName, datatype=XSD.string)) )

            #  Add Numeric ID and DiscoveryName
            graph.add( (asteroid_uri, hasNumericID, Literal(numericID, datatype=XSD.string)) )
            graph.add( (asteroid_uri, hasDiscoveryName, Literal(discoveryName, datatype=XSD.string)) )
            count+=1
        print(f"File Count: {count}")
        print(f"Last Processed: {discoveryName}")
        output_file = os.path.join(output_path, f"SOL_Asteroid_Names_{i+1}.ttl")
        temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
        next = start+iter


#  Integer Division Is Fun
def triple_remainder():
    # Initialize an empty graph
    graph = init_kg()

    remainder_path = os.path.join(data_path, "names_remainder.csv")
    with open(remainder_path, "r") as inputF:
        lines = [line.strip() for line in inputF.readlines()]
        header = (lines[0].strip()).split(",")    

    count=0
    for line in lines:
        split = line.split(",")
        numericID = split[3]
        discoveryName = split[0]
        #  Mint Asteroid
        asteroid_uri = pfs["solr"][f"Asteroid.{discoveryName.replace(' ','_')}"]
        graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]) )
        if(split[4] != ""):  #  Add Common Name when available
            commonName = split[4]
            graph.add( (asteroid_uri, hasCommonName, Literal(commonName, datatype=XSD.string)) )

        #  Add Numeric ID and DiscoveryName
        graph.add( (asteroid_uri, hasNumericID, Literal(numericID, datatype=XSD.string)) )
        graph.add( (asteroid_uri, hasDiscoveryName, Literal(discoveryName, datatype=XSD.string)) )
        count+=1
    print(f"File Count: {count}")
    print(f"Last Processed: {discoveryName}")
    output_file = os.path.join(output_path, f"SOL_Asteroid_Names_{FILE_COUNT+1}.ttl")
    temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)


triple_names()
triple_remainder()