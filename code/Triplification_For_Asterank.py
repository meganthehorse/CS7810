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
activities = ["Name", "AsteroidClassification", "Eccentricity",
              "Value","Profit", "Velocity", "MOID", "MOIDClassification"]
activity_description = ["Name", "Asteroid Classification", "Eccentricity",
                        "Value", "Profit", "Velocity", "MOID", "MOID Classification"]
observable_property = ["PhysicalProperty", "OrbitalProperty", "EconomicProperty"]

def triple_value(graph:Graph):
    ###  Adding Value[6] to SOL Ontology
    value_observation_uri = pfs["solr"][f"ValueObservation.{discovery}"]
    value_observable_property_uri = pfs["solr"][f"EconomicProperty.Value.{discovery}"]
    graph.add( (value_observation_uri, pfs["sol-ont"][f"hasFeatureOfInterest"], asteroid_uri) )
    graph.add( (value_observation_uri, pfs["sol-ont"]["hasObservableProperty"], value_observable_property_uri) )
    graph.add( (value_observable_property_uri, a, pfs["sol-ont"]["ObservableProperty"]) )

    value_activity_uri = pfs["solr"][f"ValueActivity.{discovery}"]
    graph.add( (value_activity_uri, pfs["sol-ont"]["hasDescription"], Literal(f"{activity_description[3]}", datatype=XSD.string)) )
    graph.add( (value_activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )

    #  Mint the Result and Quantity Nodes
    value_result_uri = pfs["solr"][f"Result.Value.{discovery}"]
    value_quantity_uri = pfs["solr"][f"Quantity.Value.{discovery}"]
    graph.add( (value_quantity_uri, a, pfs["sol-ont"]["Quantity"]) )
    
    value_qk_uri = pfs["solr"][f"QuantityKind.Value.{discovery}"]
    graph.add( (value_qk_uri, a, pfs["sol-ont"]["QuantityKind"]) )

    value_qv_uri = pfs["solr"][f"QuantityValue.Value.{discovery}"]
    graph.add( (value_qv_uri, a, pfs["sol-ont"]["QuantityValue"]) )

    unit_uri = pfs["solr"][f"Unit.Value.{discovery}"]    
    graph.add( (unit_uri, a, pfs["sol-ont"]["Unit"]) )
    
    value_uri = pfs["solr"][f"NumericValue.Value.{discovery}"]

    #  Declare the Result schema into the SOL Ontology
    graph.add( (value_result_uri, pfs["sol-ont"]["hasQuantity"], value_quantity_uri) )
    graph.add( (value_quantity_uri, pfs["sol-ont"]["hasQuantityKind"], value_qk_uri) ) 
    graph.add( (value_qk_uri, a, Literal("Currency", datatype=pfs["sol-qk"]["Currency"])) )

    graph.add( (value_quantity_uri, pfs["sol-ont"]["hasQuantityValue"], value_uri) )
    graph.add( (value_uri, pfs["sol-ont"]["hasUnit"], unit_uri) )

    graph.add( (unit_uri, a, Literal("USD", datatype=pfs["sol-unit"]["USD"])) )
    value_split = tokens[6].split(" ")
    if(value_split[1] == "million"):
        value=float(value_split[0])*math.pow(10, 6)
    elif(value_split[1] == "billion"):
        value=float(value_split[0])*math.pow(10, 9)
    elif(value_split[1] == "trillion"):
        value=float(value_split[0])*math.pow(10, 12)
    graph.add( (value_uri, pfs["sol-ont"]["hasNumericValue"], Literal(value, datatype=XSD.double)) ) 

    #  Connect Observation to EWP Relationships
    graph.add( (value_observation_uri, pfs["sol-ont"]["attributedTo"], agent_uri) )
    graph.add( (value_observation_uri, pfs["sol-ont"]["generatedBy"], value_activity_uri) )

    #  Connect Result to Observation        
    graph.add( (value_observation_uri, pfs["sol-ont"]["hasResult"], value_result_uri) )

def triple_profit(graph:Graph):
    profit_observation_uri = pfs["solr"][f"ProfitObservation.{discovery}"]
    profit_observable_property_uri = pfs["solr"][f"EconomicProperty.Profit.{discovery}"]
    graph.add( (profit_observation_uri, pfs["sol-ont"][f"hasFeatureOfInterest"], asteroid_uri) )
    graph.add( (profit_observation_uri, pfs["sol-ont"]["hasObservableProperty"], profit_observable_property_uri) )
    graph.add( (profit_observable_property_uri, a, pfs["sol-ont"]["ObservableProperty"]) )

    profit_activity_uri = pfs["solr"][f"ProfitActivity.{discovery}"]
    graph.add( (profit_activity_uri, pfs["sol-ont"]["hasDescription"], Literal(f"{activity_description[4]}", datatype=XSD.string)) )
    graph.add( (profit_activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )

    #  Mint the Result and Quantity Nodes
    profit_result_uri = pfs["solr"][f"Result.Profit.{discovery}"]
    profit_quantity_uri = pfs["solr"][f"Quantity.Profit.{discovery}"]
    graph.add( (profit_quantity_uri, a, pfs["sol-ont"]["Quantity"]) )
    
    profit_qk_uri = pfs["solr"][f"QuantityKind.Profit.{discovery}"]
    graph.add( (profit_qk_uri, a, pfs["sol-ont"]["QuantityKind"]) )

    profit_qv_uri = pfs["solr"][f"QuantityValue.Profit.{discovery}"]
    graph.add( (profit_qv_uri, a, pfs["sol-ont"]["QuantityValue"]) )

    unit_uri = pfs["solr"][f"Unit.Profit.{discovery}"]    
    graph.add( (unit_uri, a, pfs["sol-ont"]["Unit"]) )
    
    value_uri = pfs["solr"][f"NumericValue.Profit.{discovery}"]

    #  Declare the Result schema into the SOL Ontology
    graph.add( (profit_result_uri, pfs["sol-ont"]["hasQuantity"], profit_quantity_uri) )
    graph.add( (profit_quantity_uri, pfs["sol-ont"]["hasQuantityKind"], profit_qk_uri) ) 
    graph.add( (profit_qk_uri, a, Literal("Currency", datatype=pfs["sol-qk"]["Currency"])) )

    graph.add( (profit_quantity_uri, pfs["sol-ont"]["hasQuantityValue"], value_uri) )
    graph.add( (value_uri, pfs["sol-ont"]["hasUnit"], unit_uri) )

    graph.add( (unit_uri, a, Literal("USD", datatype=pfs["sol-unit"]["USD"])) )
    profit_split = tokens[7].split(" ")
    if(profit_split[1] == "million"):
        profit=float(profit_split[0])*math.pow(10, 6)
    elif(profit_split[1] == "billion"):
        profit=float(profit_split[0])*math.pow(10, 9)
    elif(profit_split[1] == "trillion"):
        profit=float(profit_split[0])*math.pow(10, 12)
    graph.add( (value_uri, pfs["sol-ont"]["hasNumericValue"], Literal(profit, datatype=XSD.double)) ) 


    #  Connect Observation to EWP Relationships
    graph.add( (profit_observation_uri, pfs["sol-ont"]["attributedTo"], agent_uri) )
    graph.add( (profit_observation_uri, pfs["sol-ont"]["generatedBy"], profit_activity_uri) )

    #  Connect Result to Observation        
    graph.add( (profit_observation_uri, pfs["sol-ont"]["hasResult"], profit_result_uri) )

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

#  Load in Asteroid_Distances.csv
asteroid_asterank_path = os.path.join(data_path, "Asterank_Dataset.csv")
with open(asteroid_asterank_path, "r") as inputF:
    lines = [line.strip() for line in inputF.readlines()]
    header = (lines[0].strip()).split(",")    

#  EWP
agent_uri = pfs["sol-ont"]["Agent.Asterank"]
graph.add( (agent_uri, a, pfs["sol-ont"]["Agent"]) )
graph.add( (agent_uri, pfs["sol-ont"]["hasName"], Literal("SkyLive", datatype=XSD.string)) )

# for line in lines[1:]:  #  for each asteroid
for line in lines[1:2]:  
    tokens = line.split(",")
    discovery = tokens[0]
    split = line.split(",")
    discovery = split[0].replace(" ", "_")

    #  Mint the individual Asteroid
    asteroid_uri = pfs["solr"][f"Asteroid.{discovery}"] 
    #  Declare the Asteroid Concept to the SOL Ontology
    graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]) )

    #  Numeric ID       |
    #  Common Name      | handled by Triplification_For_AsteroidNames.py
    #  Discovery Name   |

    #  Adding Orbital Data to SOL Ontology
    ##  TODO:  Add AC_Observation with OrbitalProperty
    ##  OrbitalProperty: semi-major, eccentricity, velocity, moid, moidclass

    #  Adding Economics to SOL Ontology
    ###  Adding Value[3] to SOL Ontology
    triple_value(graph)
    ###  Adding Profit[4] to SOL Ontology
    triple_profit(graph)
    
output_file = os.path.join(output_path, f"SOL_Asteroid_Asterank.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
