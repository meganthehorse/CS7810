# CS7810
Group work for WSU CS7810 - Metadata Representation Languages

# MoMO Procedure
1. Define use case/scope of use cases
2. Make CQ and gather data sources
3. Identify key notions between data and use case  
    a. Identify patterns 
4. Instantiate key notions from pattern templates
5. Add axioms for each module  
6. Assemble modules together and revise naming conventions for classes, properties, and individual names  
7. Add axioms which involve several modules and review  
8. Create OWL/RDF files with Protege and CoModIDE plug-in  

# Deliverables
1. [Narrative and Use Case](/Deliverables/use-case.md)
2. Review Gathered Data
3. [Identify Key Notions and Patterns](/Deliverables/key-notions.md)
4. [Assemble Schema Diagrams with yEd; store in /schema-diagrams:](/schema-diagrams/schema-diagram.md)  
    a. PROV-O; NameStub, AgentRole  
    b. QUDT, MODL, ODP  
5. [Axiomatization](https://docs.enslaved.org/ontology/v2/Enslaved_Documentation_V2_0-2.pdf) of individual modules
6. Revision of Schema Diagrams and Naming Conventions
7. [Axiomatization of collective modules](/Deliverables/axioms.md)
8. Protege & CoModIDE
9. Triplification with Python:  
    a. Load CSV  
    b. Init KG  
    c. graph.add(  )  
    d. graph.serialize => format: turtle  
