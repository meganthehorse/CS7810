##### Graph stuff
import os
import pandas as pd
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME

import math
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

# rdf:type shortcut
a = pfs["rdf"]["type"] #isA prefix/relationship

# Initialization shortcut
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg

# Initialize an empty graph
graph = init_kg()

#  Load in Asteroid_Distances.csv
asteroid_asterank_path = os.path.join(data_path, "Summary_of_Asteroid_Taxonomic_Classes.csv")
with open(asteroid_asterank_path, "r") as inputF:
    lines = [line.strip() for line in inputF.readlines()]
    header = (lines[0].strip()).split("|")    

#  EWP
agent_uri = pfs["sol-ont"]["Agent.Asterank"]
graph.add( (agent_uri, a, pfs["sol-ont"]["Agent"]) )
graph.add( (agent_uri, pfs["sol-ont"]["hasName"], Literal("SkyLive", datatype=XSD.string)) )

# for line in lines[1:]:  #  for each asteroid
for line in lines[1:]: 
    # Tholen Class,Albedo,Spectral Features,"SMASSII (Bus Class)",Composition,
    token = line.split("|")
    #  String parse for Classifications
    classifications = token[3]
    classifications=classifications.replace("\"", "")
    #print("Classifying the following")
    classifications = classifications.split(", ")
    #  String parse for Elemental Composition
    elements = token[4]
    elements = elements.replace("\"", "")
    elements = elements.split(",")

    for classif in classifications:
        # Mint Classification
        class_uri = pfs["solr"][f"{classif}"]
        graph.add( (class_uri, a, pfs["sol-ont"][f"SMASSIIClass"]) )
        graph.add( (class_uri, pfs["sol-ont"]["hasLabel"], Literal(classif, datatype=RDFS.label)) )
        print(f"{classif} has elements: ")
        for element in elements:
            comp_label = element.replace(" ","_")
            composition_uri = pfs["solr"][f"{classif}.{comp_label}"]
            graph.add( (composition_uri, a, pfs["sol-ont"][f"ElementalComposition.{comp_label}"]) )
            graph.add( (composition_uri, pfs["sol-ont"]["hasElement"], Literal(element, datatype=pfs["sol-ont"]["ChemicalElement"])) )
            graph.add( (class_uri, pfs["sol-ont"]["hasElementalComposition"], composition_uri) )
            print(element, end=" ")  
        print("\n")       
output_file = os.path.join(output_path, f"SOL_Asteroid_SMASSIIClass.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
