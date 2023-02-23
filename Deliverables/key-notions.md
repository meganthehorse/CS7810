#  Key Notions
##  Identified Classes
- Asteroid: owl:Role; http://ontologydesignpatterns.org/wiki/Submissions:AgentRole
  - Name; xsd:String
  - Mass, Length, Width; xsd:double
  - DistanceFromEarth, Astronomical Unit; xsd:double
  - Profit; xsd:double
  - Mineral Composition->Element; owl:Role/Thing
  - Orbit; Trajectory:  http://ontologydesignpatterns.org/wiki/Submissions:Trajectory
    - Trajectory -> Segment
    -            -> Fix ^
      - TimeEntity; SpatioTemporalEntity