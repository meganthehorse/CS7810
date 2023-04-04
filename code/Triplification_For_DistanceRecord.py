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

agent_uri = pfs["sol-ont"]["Agent.SkyLive"]
graph.add( (agent_uri, a, pfs["sol-ont"]["Agent"]) )
graph.add( (agent_uri, pfs["sol-ont"]["hasName"], Literal("SkyLive", datatype=XSD.string)) )
# activity_uri = pfs["sol-ont"]["MeasuringDistanceActivity"]
# graph.add( (activity_uri, pfs["sol-ont"]["hasDescription"], Literal("Measuring Distance", datatype=XSD.string)) )
# graph.add( (activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )

for line in lines[1:]:  # for each asteroid
    split = line.split(",")
    name = split[0].replace(" ","_")
    #  Mint the individual Asteroid
    asteroid_uri = pfs["solr"][f"Asteroid.{name}"] 
    #  Declare the Asteroid Concept to the SOL Ontology
    graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]) )
    index = 1  # Index for header column
    for distance in split[1:]:   # for each column per asteroid
        if(str(distance) == ""): 
            continue # if blank check
        monthyear = header[index]
        #  Mint the individual distance record per asteroid
        distance_record_uri = pfs["solr"][f"{monthyear}DistanceRecord.{name}."]
        #  Declare the individual DR Concept to the SOL Ontology
        graph.add( (distance_record_uri, a, pfs["sol-ont"]["DistanceRecord"]) )
        #  Connect the Asteroid Concept to the DR Concept
        graph.add( (asteroid_uri, pfs["sol-ont"]["hasDistanceRecord"], distance_record_uri) )

        #  Mint the Result and Quantity Nodes
        result_uri = pfs["solr"][f"{monthyear}Result.{name}"]
        quantity_uri = pfs["solr"][f"{monthyear}Quantity.{name}"]
        graph.add( (quantity_uri, a, pfs["sol-ont"]["Quantity"]) )
        # quantity_kind_uri = pfs["solr"][f"QuantityKind.{name}.{monthyear}"]
        # graph.add( (quantity_kind_uri, a, pfs["sol-ont"]["QuantityKind"]) )
        quantity_value_uri = pfs["solr"][f"{monthyear}QuantityValue.{name}"]
        graph.add( (quantity_value_uri, a, pfs["sol-ont"]["QuantityValue"]) )
        # unit_uri = pfs["solr"][f"Unit.{name}.{monthyear}"]
        # graph.add( (unit_uri, a, pfs["sol-ont"]["Unit"]) )
        #value_uri = pfs["solr"][f"NumericValue.{name}.{monthyear}"]

        #  Declare the Result schema into the SOL Ontology      
        graph.add( (result_uri, pfs["sol-ont"]["hasQuantity"], quantity_uri) )
        # graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityKind"], quantity_kind_uri) ) 
        graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityKind"], Literal("Distance", datatype=pfs["sol-qk"]["Distance"])) )

        graph.add( (quantity_uri, pfs["sol-ont"]["hasQuantityValue"], quantity_value_uri) )        
        # graph.add( (unit_uri, a, Literal("au", datatype=pfs["sol-unit"]["au"])) )
        graph.add( (quantity_value_uri, pfs["sol-ont"]["hasUnit"], Literal("au", datatype=pfs["sol-unit"]["au"])) )
        graph.add( (quantity_value_uri, pfs["sol-ont"]["hasNumericValue"], Literal(distance, datatype=XSD.double)) ) 
        
        #  Add TemporalExtent Triple to SOL Ontology
        time_uri = pfs["solr"][f"{monthyear}TemporalExtent.{name}"]
        graph.add( (time_uri, pfs["sol-ont"]["recordedAt"], Literal(monthyear, datatype=TIME.MonthOfYear)))
        
        #  Connect Result and Time to DR
        graph.add( (distance_record_uri, pfs["sol-ont"]["hasResult"], result_uri) )
        graph.add( (distance_record_uri, pfs["sol-ont"]["hasTemporalExtent"], time_uri) )

        #  Connect DR to EWP Relationships
        activity_uri = pfs["sol-ont"][f"MeasuringDistanceActivity.{name}.{monthyear}"]
        graph.add( (activity_uri, pfs["sol-ont"]["hasDescription"], Literal("Measuring Distance", datatype=XSD.string)) )
        graph.add( (activity_uri, pfs["sol-ont"]["performedBy"], agent_uri) )

        graph.add( (distance_record_uri, pfs["sol-ont"]["attributedTo"], agent_uri) )
        graph.add( (distance_record_uri, pfs["sol-ont"]["generatedBy"], activity_uri) )

        
        #  Connect DR to Asteroid
        graph.add( (asteroid_uri, pfs["sol-ont"]["hasDistanceRecord"], distance_record_uri) )
        index+=1  #  next monthyear column




output_file = os.path.join(output_path, f"SOL_Asteroid_DistanceRecord_Results.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
