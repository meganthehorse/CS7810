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