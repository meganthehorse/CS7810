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
a = pfs["rdf"]["type"]

#  Load Asteroid Data into a pandas df

#  Asteroid Column Labels
asteroid_op_names = ['Name',
                     'JAN23','MAY23','AUG23','NOV23',
                     'JAN24','MAY24','AUG24','NOV24',
                     'JAN25','MAY25','AUG25','NOV25',
                     'JAN26','MAY26','AUG26','NOV26',
                     'JAN27','MAY27','AUG27','NOV27',
                     'JAN28','MAY28','AUG28','NOV28',
                     'JAN29','MAY29','AUG29','NOV29',
                     'JAN30','MAY30','AUG30','NOV30']

# Initialize an empty graph
graph = init_kg()

# Initialize from a file
# filename = "path/to/file"
# with open(filename, "w") as f:
#     graph.parse(f)

#  Load in Asteroid_Distances.csv
asteroid_distances_file = os.path.join(data_path, "Asteroid_Distances.csv")
distance_df = pd.read_csv(asteroid_distances_file, header=0)
#  Pairing Column Labels to prefix dictionary
asteroid_op_uris = dict()
# for asteroid_op_name in asteroid_op_names:  # for each column label
#     asteroid_op_uri = pfs["solr"][f"soloflife.{asteroid_op_name}"]
#     asteroid_op_uris[asteroid_op_name] = asteroid_op_uri

for i in range(len(distance_df["Name"])):  
    asteroid_uri = pfs["solr"][f"{distance_df['Name'][i]}"]
    print("Debug: " + asteroid_uri)
    for col in asteroid_op_names:    
        graph.add( (asteroid_uri, a, pfs["sol-ont"]["Asteroid"]))
        
        # print(distance_df[col][i])
        #  Link URI to each Asteroid

output_file = os.path.join(output_path, f"SOL_Asteroid.ttl")
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
