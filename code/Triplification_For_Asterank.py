#####
#
# This triplification for Asterank_Dataset.csv
# skips MOID Classification as a pattern has not
# been described for Classifiers outside the AsteroidClassification
#
#####


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
# Type,a (AU),e,
# Value ($),Est. Profit ($),Δv (km/s),MOID (AU),Group
CV_QK = ["AsteroidClassification", "Semi-MajorAxis", "Eccentricity",
              "Value","Profit", "Velocity", "MOID", "MOIDClassification"]
CV_UNITS = ["","au","au",
            "Currency","Currency","kms","au","group"]
ACTIVITIES = ["AsteroidClassification", "Semi-MajorAxis", "Eccentricity",
              "Value","Profit", "Velocity", "MOID", "MOIDClassification"]
ACTIVITY_DESC = ["Asteroid Classification", "Semi-Major Axis","Eccentricity",
                        "Value", "Profit", "Velocity", "MOID", "MOID Classification"]
OBSERVABLE_PROPERTIES = ["PhysicalProperty", "OrbitalProperty", "EconomicProperty"]

def triple_orbital(graph:Graph, data, index):
    activity = ACTIVITIES[index]
    description = ACTIVITY_DESC[index]
    qk = CV_QK[index]
    unit = CV_UNITS[index]
    observation_uri = pfs["solr"][f"Observation.{activity}.{discovery}"]
    observable_property_uri = pfs["solr"][f"OrbitalProperty.{activity}.{discovery}"]
    graph.add( (observation_uri, pfs["sol-ont"][f"hasFeatureOfInterest"], asteroid_uri) )
    graph.add( (observation_uri, pfs["sol-ont"]["hasObservableProperty"], observable_property_uri) )
    graph.add( (observable_property_uri, a, pfs["sol-ont"]["ObservableProperty"]) )

    activity_uri = pfs["solr"][f"Activity.{activity}.{discovery}"]
    graph.add( (activity_uri, pfs["sol-ont"]["hasDescription"], Literal(f"{description}", datatype=XSD.string)) )
    graph.add( (activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )
    
    #  Mint the Result and Quantity Nodes
    result_uri = pfs["solr"][f"Result.{activity}.{discovery}"]
    graph.add( (result_uri, a, pfs["sol-ont"]["Result"]) )
    quantity_uri = pfs["solr"][f"Quantity.{activity}.{discovery}"]
    graph.add( (quantity_uri, a, pfs["sol-ont"]["Quantity"]) )
        
    qk_uri = pfs["solr"][f"QuantityKind.{activity}.{discovery}"]
    graph.add( (qk_uri, a, pfs["sol-ont"]["QuantityKind"]) )

    qv_uri = pfs["solr"][f"QuantityValue.{activity}.{discovery}"]
    graph.add( (qv_uri, a, pfs["sol-ont"]["QuantityValue"]) )

    unit_uri = pfs["solr"][f"Unit.{activity}.{discovery}"]    
    graph.add( (unit_uri, a, pfs["sol-ont"]["Unit"]) )
    
    value_uri = pfs["solr"][f"NumericValue.{activity}.{discovery}"]

    #  Declare the Result schema into the SOL Ontology
    graph.add( (result_uri, pfs["sol-ont"]["hasQuantity"], quantity_uri) )
    graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityKind"], qk_uri) ) 
    graph.add( (qk_uri, a, Literal(qk, datatype=pfs["sol-qk"][qk])) )

    graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityValue"], value_uri) )
    graph.add( (value_uri, pfs["sol-ont"]["hasUnit"], unit_uri) )

    graph.add( (unit_uri, a, Literal(unit, datatype=pfs["sol-unit"][unit])) )
    graph.add( (value_uri, pfs["sol-ont"]["hasNumericValue"], Literal(data, datatype=XSD.double)) ) 

    #  Connect Observation to EWP Relationships
    graph.add( (observation_uri, pfs["sol-ont"]["attributedTo"], agent_uri) )
    graph.add( (observation_uri, pfs["sol-ont"]["generatedBy"], activity_uri) )

    #  Connect Result to Observation        
    graph.add( (observation_uri, pfs["sol-ont"]["hasResult"], result_uri) )


def triple_economic(graph:Graph, numeric, index):
    activity = ACTIVITIES[index]
    observation_uri = pfs["solr"][f"{activity}Observation.{discovery}"]
    observable_property_uri = pfs["solr"][f"EconomicProperty.{activity}.{discovery}"]
    graph.add( (observation_uri, pfs["sol-ont"][f"hasFeatureOfInterest"], asteroid_uri) )
    graph.add( (observation_uri, pfs["sol-ont"]["hasObservableProperty"], observable_property_uri) )
    graph.add( (observable_property_uri, a, pfs["sol-ont"]["ObservableProperty"]) )

    activity_uri = pfs["solr"][f"Activity.{activity}.{discovery}"]
    graph.add( (activity_uri, pfs["sol-ont"]["hasDescription"], Literal(f"{ACTIVITY_DESC[index]}", datatype=XSD.string)) )
    graph.add( (activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )
    
    #  Mint the Result and Quantity Nodes
    result_uri = pfs["solr"][f"Result.{activity}.{discovery}"]
    graph.add( (result_uri, a, pfs["sol-ont"]["Result"]) )
    quantity_uri = pfs["solr"][f"Quantity.{activity}.{discovery}"]
    graph.add( (quantity_uri, a, pfs["sol-ont"]["Quantity"]) )
        
    qk_uri = pfs["solr"][f"QuantityKind.{activity}.{discovery}"]
    graph.add( (qk_uri, a, pfs["sol-ont"]["QuantityKind"]) )

    qv_uri = pfs["solr"][f"QuantityValue.{activity}.{discovery}"]
    graph.add( (qv_uri, a, pfs["sol-ont"]["QuantityValue"]) )

    unit_uri = pfs["solr"][f"Unit.{activity}.{discovery}"]    
    graph.add( (unit_uri, a, pfs["sol-ont"]["Unit"]) )
    
    value_uri = pfs["solr"][f"NumericValue.{activity}.{discovery}"]

    #  Declare the Result schema into the SOL Ontology
    graph.add( (result_uri, pfs["sol-ont"]["hasQuantity"], quantity_uri) )
    graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityKind"], qk_uri) ) 
    graph.add( (qk_uri, a, Literal("Currency", datatype=pfs["sol-qk"]["Currency"])) )

    graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityValue"], value_uri) )
    graph.add( (value_uri, pfs["sol-ont"]["hasUnit"], unit_uri) )

    graph.add( (unit_uri, a, Literal("USD", datatype=pfs["sol-unit"]["USD"])) )
    split = numeric.split(" ")
    if(split[1] == "million"):
        value=float(split[0])*math.pow(10, 6)
    elif(split[1] == "billion"):
        value=float(split[0])*math.pow(10, 9)
    elif(split[1] == "trillion"):
        value=float(split[0])*math.pow(10, 12)
    graph.add( (value_uri, pfs["sol-ont"]["hasNumericValue"], Literal(value, datatype=XSD.double)) ) 

    #  Connect Observation to EWP Relationships
    graph.add( (observation_uri, pfs["sol-ont"]["attributedTo"], agent_uri) )
    graph.add( (observation_uri, pfs["sol-ont"]["generatedBy"], activity_uri) )

    #  Connect Result to Observation        
    graph.add( (observation_uri, pfs["sol-ont"]["hasResult"], result_uri) )

def triple_type(graph:Graph, type, index=1):
    activity = ACTIVITIES[index]
    #  Mint
    classification_uri = pfs["solr"][f"{activity}.{discovery}"]
    graph.add( (classification_uri, a, pfs["sol-ont"]["AsteroidClassification"]) )
    smassii_uri = pfs["solr"][f"SMASSII.{discovery}"]
    graph.add( (smassii_uri, a, pfs["sol-ont"]["SMASSIIClass"]) )
    graph.add( (asteroid_uri, pfs["sol-ont"][f"hasAsteroidClassification"], classification_uri) )

    #  Declare
    graph.add( (classification_uri, pfs["sol-ont"]["hasSMASSIIClass"], smassii_uri) )
    graph.add( (smassii_uri, pfs["sol-ont"]["hasLabel"], Literal(type, datatype=RDFS.label)) )
    ##  TODO:  Confirm ElementalComposition link from Triplification of Taxonomy
    activity_uri = pfs["solr"][f"Activity.{activity}.{discovery}"]
    graph.add( (activity_uri, pfs["sol-ont"]["hasDescription"], Literal(f"{ACTIVITY_DESC[index]}", datatype=XSD.string)) )
    graph.add( (activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )

    #  Connect AC to EWP Relationships
    graph.add( (classification_uri, pfs["sol-ont"]["attributedTo"], agent_uri) )
    graph.add( (classification_uri, pfs["sol-ont"]["generatedBy"], activity_uri) )

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
    # Discovery Name,Common Name,Asterank Name,Type,a (AU),e,Value ($),Est. Profit ($),Δv (km/s),MOID (AU),Group
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
    triple_type(graph, tokens[3])
    ##  OrbitalProperty: semi-major, eccentricity, velocity, moid
    orbitIndices = [4, 5, 8, 9]
    for i in orbitIndices:
        data = tokens[i]
        triple_orbital(graph, data, i-3)
    #  Adding Economics to SOL Ontology
    ###  Adding Value[3] to SOL Ontology
    economic_data = [tokens[6], tokens[7]]
    index = 3
    for data in economic_data:
        triple_economic(graph, data, index)
        index+=1
    # triple_value(graph)
    ###  Adding Profit[4] to SOL Ontology
    # triple_profit(graph)
    
output_file = os.path.join(output_path, f"SOL_Asteroid_Asterank.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
