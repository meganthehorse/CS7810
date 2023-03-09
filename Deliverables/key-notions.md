#  Key Notions
##  Identified Classes
- Asteroid: owl:Role; http://ontologydesignpatterns.org/wiki/Submissions:AgentRole
  - Name; xsd:String
  - Mass, Length, Width; xsd:double
  - DistanceFromEarth, Astronomical Unit; xsd:double
  - Profit; xsd:double
  - Asteroid Type -> Mineral Composition->Element; owl:Role/Thing
  - Orbit; Trajectory:  http://ontologydesignpatterns.org/wiki/Submissions:Trajectory
    - Trajectory -> Segment
    -            -> Fix ^
      - TimeEntity; SpatioTemporalEntity

* Will require review of sbdb columns

## Potential Key-Notions (needs discussed)

###  Asteroid  
An Asteroid is represented by NASA as an object that orbits the sun of the Sol Solar System measuring 33 feet (10 meters) to 329 miles (530 kilometers).  The Asteroid as a key-notion can be derived as an OWL AgentRole when viewed alongside other celestial bodies found in space.  For the SOL of Life, the Asteroid represents an entity that provides a profit for exomining operations.

- Asteroid
  - The asteroid is the focus of the knowledge graph, combining all other key notions.

###  AsteroidDistances (DistanceRecording, DistanceSnapshots?)
The end-goal of SOL of Life is to provide insight for whether an Asteroid is within a means of distance for exomining companies to travel to for mineral extraction operations.  As such, the spatial coordinates of an Asteroid is less important than the actual distance from Earth, which acts as a baseline for exomining operations.  The distance from Earth is collected for the months of January and July over a range of years to which can be used within the query

- Orbital_Properties
  - The asteroid has properties related to it's spacial orbit.  These properties include average velocity, average distance from earth, and a list of estimates for the asteroids' distance from earth at a given date. 

- Distance_Estimate
  - The distance estimate is included under orbital properties and ties together a month, year, and estimated distance from earth  

###  AsteroidClassification (rather simply Classification)
The derived mineralogy of an Asteroid is a prediction based from infrared readings as traveling to each individual asteroid remains an unrealistic task.  As such, infrared reflections and readings are compared for similarities against known Earth minerals and denote the components from the Asteroid's surface.  The infrared data has been collected to formulate classifications based on similarity of readings.  SOL of Life utilizes the SMASS classification labels in order to connect an Asteroid to the elemental composition.

###  
- Assigned_Properties
  - The asteroid has a set of human-assigned properties that are used to characterize and define the asteroid.  These include the "worth" metrics and "identification" properties.  The "worth" metrics include estimated profit and estimated total value.  The "identification" metrics include asteroid name and classification.

