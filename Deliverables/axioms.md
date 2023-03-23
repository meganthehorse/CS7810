# SOL of Life

![All Together](/schema-diagrams/all-together/all-together.jpg)  

## Asteroid
![Asteroids](/schema-diagrams/asteroid/asteroid.jpg)  

### Axioms
* `axiom in manchester syntax` <br />
Asteroid is a subclass of Feature of Interest  
* `axiom in manchester syntax` <br />
NearEarthAsteroid is a subclass of Asteroid (that has a semi-major axis less than x au)
* `axiom in manchester syntax` <br />

* `axiom in manchester syntax` <br />

* `axiom in manchester syntax` <br />
  

## AsteroidClassification
![Asteroid Classification Types](/schema-diagrams/asteroid-classification/asteroid-classification.jpg)

### Axioms
* `axiom in manchester syntax` <br />
AsteroidClassification is a subclass of EntityWithProvenance  
* `axiom in manchester syntax` <br />
  
* `axiom in manchester syntax` <br />
  

## DistanceRecord
![image](/schema-diagrams/distance-record/distance-record.jpg)

### Axioms
*  `axiom in manchester`  
DistanceRecord is a subclass of EntityWithProvenance
* `axiom in manchester syntax` <br />
  
* `axiom in manchester syntax` <br />
  
  
## Entity With Provenance
![image](/schema-diagrams/entity-with-provenance/entity-with-provenance.jpg)

###  Axioms
*  `axiom in manchester`  
TO BE ADOPTED by [MODL](https://docs.enslaved.org/ontology/v2/Enslaved_Documentation_V2_0-2.pdf)  

##  Observation
![image](/schema-diagrams/observation/observation.jpg)  

###  Axioms
*  `axiom in manchester`  
Observation is a subclass of EntityWithProvenance  
*  `axiom in manchester`  
Observation has at least one ObservableProperty  
*  `axiom in manchester`  
Observation has at least one Result  

##  Result
![image](/schema-diagrams/result/Result.jpg)

###  Axioms
*  `axiom in manchester`  
TO BE ADOPTED by MODL  
*  `axiom in manchester`  
Result has at least one Quantity  
*  `axiom in manchester`  
Quantity has at least one QuantityKind  
