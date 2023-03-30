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
"time": TIME,
"qudt": Namespace("http://qudt.org/schema/qudt/"),
"soqk": Namespace("http://qudt.org/vocab/quantitykind/")
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
    # for distances in split[1:]:
    # lets just look at 1 time range...
    for distance in split[1:2]:
        monthyear = header[index]
        #  Mint the individual distance record per asteroid
        distance_record_uri = pfs["solr"][f"DistanceRecord.{name}.{monthyear}"]
        #  Declare the individual DR Concept to the SOL Ontology
        graph.add( (distance_record_uri, a, pfs["sol-ont"]["DistanceRecord"]) )
        #  Connect the Asteroid Concept to the DR Concept
        graph.add( (asteroid_uri, pfs["sol-ont"]["hasDistanceRecord"], distance_record_uri) )

        #  Result->Quantity->QuantityKind (au)
        #                  ->QuantityValue (actual recording) ->hasUnit: Unit
        #                                                     ->hasNumericValue: xsdDouble
        #  Mint the Result and Quantity Nodes
        result_uri = pfs["solr"][f"Result.{name}.{monthyear}"]
        quantity_uri = pfs["sol-ont"][f"Result.Quantity.{name}.{monthyear}"]
        graph.add( (quantity_uri, a, pfs["modl"]["Quantity"]) )
        quantity_kind_uri = pfs["sol-ont"][f"Quantity.QuantityKind.{name}.{monthyear}"]
        graph.add( (quantity_kind_uri, a, pfs["modl"]["QuantityKind"]) )
        quantity_value_uri = pfs["sol-ont"][f"Quantity.QuantityValue.{name}.{monthyear}"]
        graph.add( (quantity_value_uri, a, pfs["modl"]["QuantityValue"]) )
        qudt_unit_uri = pfs["sol-ont"][f"QuantityValue.Unit.{name}.{monthyear}"]
        graph.add( (qudt_unit_uri, a, pfs["modl"]["Unit"]) )
        qudt_value_uri = pfs["sol-ont"][f"QuantityValue.NumericValue.{name}.{monthyear}"]

        #  Declare the Result schema into the SOL Ontology      
        # TODO:
        #  - Double Check Validity of Controlled Vocabulary usage below
        #  - https://qudt.org/vocab/quantitykind/Distance
        #    qudt:hasQuantityKind quantitykind:Distance ;
        graph.add( (result_uri, pfs["qudt"]["hasQuantity"], quantity_uri) )
        graph.add( (quantity_uri, pfs["qudt"]["hasQuantityKind"], quantity_kind_uri) ) 
        graph.add( (quantity_uri, pfs["qudt"]["hasQuantityKind"], Literal("Distance", datatype=pfs["soqk"]["Distance"])) )

        graph.add( (quantity_uri, pfs["qudt"]["hasQuantityValue"], quantity_value_uri) )        
        graph.add( (quantity_value_uri, pfs["qudt"]["hasUnit"], qudt_unit_uri) )
        graph.add( (qudt_unit_uri, a, Literal("au", datatype=pfs["soqk"]["Distance"])) )
        #  TODO:  Is this how you handle URI's for data values?
        graph.add( (qudt_value_uri, pfs["soqk"]["hasNumericValue"], qudt_value_uri) )
        graph.add( (qudt_value_uri, pfs["xsd"]["double"], Literal(distance, datatype=XSD.double)) ) 
        
        #  Add TemporalExtent Triple to SOL Ontology
        time_uri = pfs["solr"][f"time.{name}.{monthyear}"]
        graph.add( (time_uri, pfs["sol-ont"]["recordedAt"], Literal(monthyear, datatype=TIME.MonthOfYear)))
        
        #  Connect Result and Time to DR
        graph.add( (distance_record_uri, pfs["sol-ont"]["hasResult"], result_uri) )
        graph.add( (distance_record_uri, pfs["sol-ont"]["hasTemporalExtent"], time_uri) )

        #  Connect DR to Asteroid
        graph.add( (asteroid_uri, pfs["sol-ont"]["hasDistanceRecord"], distance_record_uri) )
        index+=1  #  next monthyear column



output_file = os.path.join(output_path, f"SOL_Asteroid_DistanceRecord_Results.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
