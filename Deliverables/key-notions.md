#  Key Notions
##  Identified Classes

###  Asteroid  
The domain of space objects are broken into three subcategories: Artificial Space Objects, Space Weather Phenomena, and Natural Space Objects.  Asteroids exist as a Natural Space Object where object can be further defined as a material object.  An Asteroid is represented by NASA as an object that orbits the sun of the Sol Solar System measuring 33 feet (10 meters) to 329 miles (530 kilometers).  For the SOL of Life, the only celestial body to be concerned with is Asteroid; therefore, the derived understanding begins with an OWL Thing consisting of multiple properties; such as, labeled naming conventions and quantitative measurable components of velocity, semi-major axis, and minimum orbit intersection distance.  Researchers have also predicted properties that benefit exomining operations such as the average profit gained after a mining excavation with consideration of the available valuable materials.  A subsumption is made for Asteroids into Near-Earth Asteroids when their semi-major axis measurement is within a threshold.  The SOSA pattern best reflects the usage of SOL of Life's knowledge graph with respect to the layer of Observations. Asteroids can be represented as a Feature of Interest with an Observation that has Observable Properties.  

###  ObservableProperty  
Data that is represented by Asteroids can be described as Observations from the SOSA pattern which consists of the property that describes the observation along with the quantifiable value.  The description of the property follows SOSA's ObservableProperty pattern, and the value follows SOSA's Result pattern.  With that in mind, the measurable data; such as, mass, velocity, and SMASII Classification, are represented as an instance of an Observation.

###  DistanceRecording as an Observation  
The end-goal of SOL of Life is to provide insight at a specific point of time for whether an Asteroid is within a means of distance for exomining companies to travel to for mineral extraction operations.  As such, the spatial coordinates of an Asteroid is less important than the actual distance from Earth, which acts as a baseline for exomining operations.  The distance from Earth is collected every quarter in a 10 year range.  

###  AsteroidType as an Observation
The derived elemental composition of an Asteroid is a prediction based from infrared readings as traveling to each individual asteroid remains an unrealistic task.  As such, infrared reflections and readings are compared for similarities against known Earth elements and denote the components from the Asteroid's surface.  The infrared data has been collected to formulate classifications among clusters of all asteroids for similarities of readings.  With respect to the SOSA Observation pattern, the infrared readings produce observable properties of elemental compositions.  The infrared readings and cluster family of similar asteroids result in a SMASSII classification which exists as a literal label.


##  Dataset  

Source:  [Nasa-JPL: SBDB](https://ssd.jpl.nasa.gov/tools/sbdb_query.html)  
- Nasa-JPL Small Body Database (SBDB) serves as a well established and primary source for data on asteroids as well as other "small bodies".  The SBDB includes extensive information on orbital, physical, and historical properties.  SOL of Life will utilize the SBDB for data relating to orbital properties for asteroids.  

Source: [Asterrank](https://www.asterank.com/)
- Asterank is built atop Nasa's Small Body Database to provide asteroid orbital data as well as estimates for asteroid value and distance metrics.  SOL of Life will contain a subset of Asterrank's data focusing on asteroid worth and distance metrics.

Source: [MP3C](https://mp3c.oca.eu/)
- Similar to the Nasa-JPL Small Body Database, MP3C Asteroid Database also serves as a source for physcial and orbital data on asteroids.  MP3C's database is maintained by the Observatoire de la Côte d'Azur and includes measurements and observations on the orbital and physical properties of asteroids.  SOL of Life will utilize the MP3C's database as a secondary source for orbital data on asteroids.  

Source:  [Sky Live](https://theskylive.com/)
- Historical and Predictive measurements of celestial bodies given their orbital trajectory can be recorded from the Sky Live tool.

##  SOSA Pattern
Source: [SOSA](https://www.w3.org/TR/vocab-ssn/)  

##  DataTypes  
Source:  [Unified Code for Units of Measure in RDF:  cdt:ucum](https://hal.science/hal-01885337/document)
Source: [rdfs: label](https://www.w3.org/2000/01/rdf-schema#label)
Source: [QUDT](https://www.qudt.org/)
Source: [DBOntology for Chemical Elements:  dbo:ChemicalElement](https://dbpedia.org/ontology/ChemicalElement)
