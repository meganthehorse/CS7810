##### Graph stuff
import os
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME

import math
#  Directory Path Parameters
data_path = "../Dataset/"
output_path = "../output/"

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

reference_IDs = ["e","a","q","i","node","peri","M","period_y","n","Q","D"]

reference = ["Orbital Eccentricity", "Semi-Major Axis", "Perihelion Distance", 
             "Inclination", "Longitude of the Ascending Node", "Argument of Perihelion",
             "Mean Anomaly", "Orbital Period", "Mean Motion", "Aphelion Distance",
             "Diameter"]

units = ["None", "au", "au", "deg","deg","deg","deg","y","deg/d","au","km"]

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

#  Load in nasajpl-sbdl.csv
nasajpl_path = os.path.join(data_path, "nasajpl-sbdl.csv")
with open(nasajpl_path, "r") as inputF:
    lines = [line.strip() for line in inputF.readlines()]
    header = (lines[0].strip()).split(",")    

#  EWP
agent_uri = pfs["sol-ont"]["Agent.NASA-JPL"]
graph.add( (agent_uri, a, pfs["sol-ont"]["Agent"]) )
graph.add( (agent_uri, pfs["sol-ont"]["hasName"], Literal("NASA-JPL", datatype=XSD.string)) )

# for line in lines[1:]:  #  for each asteroid
for line in lines[1:]:  
    tokens = line.split(",")
    Asteroid_ID = tokens[0]

    #  Mint the individual Asteroid
    asteroid_uri = pfs["solr"][f"Asteroid.{Asteroid_ID}"] 
    #  Declare the Asteroid Concept to the SOL Ontology
    graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]))

    for index, property in enumerate(reference_IDs):

        obs_id = f"{property}_Observation"
        act_id = f"{property}_Activity"

        observation_uri = pfs["solr"][f"{obs_id}.{Asteroid_ID}"]
        propertyType = "Orbital"

        if property == "H": propertyType = "Physical"
        
        observable_property_uri = pfs["solr"][f"{propertyType}Property.{obs_id}.{Asteroid_ID}"]
        graph.add( (observation_uri, pfs["sol-ont"][f"hasFeatureOfInterest"], asteroid_uri) )
        graph.add( (observation_uri, pfs["sol-ont"]["hasObservableProperty"], observable_property_uri) )
        graph.add( (observable_property_uri, a, pfs["sol-ont"]["ObservableProperty"]) )

        activity_uri = pfs["solr"][f"{act_id}.{Asteroid_ID}"]
        graph.add( (activity_uri, pfs["sol-ont"]["hasDescription"], Literal(f"{reference[index]}", datatype=XSD.string)) )
        graph.add( (activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )

        #  Mint the Result and Quantity Nodes
        result_uri = pfs["solr"][f"Result.{obs_id}.{Asteroid_ID}"]
        quantity_uri = pfs["solr"][f"Quantity.{obs_id}.{Asteroid_ID}"]
        graph.add( (quantity_uri, a, pfs["sol-ont"]["Quantity"]) )
        
        qk_uri = pfs["solr"][f"QuantityKind.{obs_id}.{Asteroid_ID}"]
        graph.add( (qk_uri, a, pfs["sol-ont"]["QuantityKind"]) )

        qv_uri = pfs["solr"][f"QuantityValue.{obs_id}.{Asteroid_ID}"]
        graph.add( (qv_uri, a, pfs["sol-ont"]["QuantityValue"]) )

        unit_uri = pfs["solr"][f"Unit.{obs_id}.{Asteroid_ID}"]    
        graph.add( (unit_uri, a, pfs["sol-ont"]["Unit"]) )
        
        value_uri = pfs["solr"][f"NumericValue.{obs_id}.{Asteroid_ID}"]

        #  Declare the Result schema into the SOL Ontology
        graph.add( (result_uri, pfs["sol-ont"]["hasQuantity"], quantity_uri) )
        graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityKind"], qk_uri) ) 
        
        ##################################################################
        # This needs fixed probably, unsure what to use for Quantity Kind  
        graph.add( (qk_uri, a, Literal(f"{property}", datatype=pfs["sol-qk"][f"{property}"])) )

        graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityValue"], value_uri) )
        graph.add( (value_uri, pfs["sol-ont"]["hasUnit"], unit_uri) )

        unit = units[index]
        graph.add( (unit_uri, a, Literal(f"{unit}", datatype=pfs["sol-unit"][f"{unit}"])) )

        value = tokens[index+3]
        if value == '': 
            graph.add( (value_uri, pfs["sol-ont"]["hasNumericValue"], Literal("N/A", datatype=XSD.string)) ) 
        else:
            graph.add( (value_uri, pfs["sol-ont"]["hasNumericValue"], Literal(tokens[index+3], datatype=XSD.double)) )
        
        #  Connect Observation to EWP Relationships
        graph.add( (observation_uri, pfs["sol-ont"]["attributedTo"], agent_uri) )
        graph.add( (observation_uri, pfs["sol-ont"]["generatedBy"], activity_uri) )

        #  Connect Result to Observation        
        graph.add( (observation_uri, pfs["sol-ont"]["hasResult"], result_uri) )

    
output_file = os.path.join(output_path, "SOL_NASA.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)