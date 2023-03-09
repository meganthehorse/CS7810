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

- Asteroid
  - The asteroid is the focus of the knowledge graph, combining all other key notions.

- Assigned_Properties
  - The asteroid has a set of human-assigned properties that are used to characterize and define the asteroid.  These include the "worth" metrics and "identification" properties.  The "worth" metrics include estimated profit and estimated total value.  The "identification" metrics include asteroid name and classification.

- Orbital_Properties
  - The asteroid has properties related to it's spacial orbit.  These properties include average velocity, average distance from earth, and a list of estimates for the asteroids' distance from earth at a given date. 

- Distance_Estimate
  - The distance estimate is included under orbital properties and ties together a month, year, and estimated distance from earth  
