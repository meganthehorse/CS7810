# List of Axiomatizations
# Table of Contents
1. [Asteroid Schema](#Asteroid)
2. [AsteroidClassification Schema](#AsteroidClassification)
3. [DistanceRecord Schema](#DistanceRecord)
4. [EntityWithProvenance](#EntityWithProvenance)
6. [Observation Schema](#Observation)
7. [Result Schema](#Result)
8. [All-Together Schema](#all-together)

## Asteroid
- Asteroid is a subclass of Feature of Interest  
- NearEarthAsteroid is a subclass of Asteroid (that has a semi-major axis less than x au)

## AsteroidClassification
- AsteroidClassification is a subclass of EntityWithProvenance

## DistanceRecord
- DistanceRecord is a subclass of EntityWithProvenance

## EntityWithProvenance
- TO BE ADOPTED by MODL

## Observation
- Observation is a subclass of EntityWithProvenance 
- Observation has at least one ObservableProperty
- Observation has at least one Result

## Result
- TO BE ADOPTED by MODL
- Result has at least one Quantity
- Quantity has at least one QuantityKind
- 

## All-Together
