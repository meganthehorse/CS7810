# Validation

## 1. Top 5 Most Frequently Occurring Minerals
**Competency Question:** "What are the top 5 most frequently occuring minerals within 1.5 astronomical units from Earth in 2024?"

**Bridged Datasets:** 
sbdb_jpl_asteroids_with_constraints.csv, Asterank.csv, Summary_of_Asteroid_Taxonomic_Classes.csv

**SPARQL Query:**
```sql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX so: <http://schema.org/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX sol-ont: <http://soloflife.org/lod/ontology/>
PREFIX solr: <http://soloflife.org/lod/resource/>

SELECT (?e as ?Element) (count(?e) as ?CountOfElement)
WHERE {
  {
    ?asteroid a sol-ont:Asteroid .
    ?asteroid sol-ont:hasCommonName ?name .
    ?asteroid sol-ont:hasDistanceRecord ?record .
    ?record sol-ont:hasTemporalExtent ?te .
    ?te sol-ont:recordedAt ?time .
    ?asteroid sol-ont:hasAsteroidClassification ?type .
    ?type sol-ont:hasSMASSIIClass ?class.
    ?class sol-ont:hasElementalComposition ?EC .
    ?EC sol-ont:hasElement ?e .
    ?record sol-ont:hasResult ?r. 
    ?r sol-ont:hasQuantity ?q.
    ?q sol-ont:hasQuantityValue ?qv .
    ?qv sol-ont:hasNumericValue ?distance .
    FILTER(
      ?distance < 1.5 &&
      (?time >= "2024-01"^^xsd:gYearMonth &&
      ?time < "2025-01"^^xsd:gYearMonth)
    )
  } 
}
GROUP BY ?e
ORDERBY DESC (?CountOfElement)
LIMIT 5
```

**Results:**
|Element |CountOfElement|
|--------|--------------|
|iron    |10            |
|ammonia |7             |
|hydrogen|7             |
|nitrogen|7             |
|cobalt  |6             |

## 2. Top 3 Most Occurring Asteroid Types
**Competency Question:** "What are the top 3 most occuring asteroid types within 1.5au from Earth in 2025?"

**Bridged Datasets:** sbdb_jpl_asteroids_with_constraints.csv, Asterank.csv, Summary_of_Asteroid_Taxonomic_Classes.csv

**SPARQL Query:**
```sql
SELECT (?class as ?AsteroidType) (count(?class) as ?CountOfTypes)
WHERE {
  {
    ?asteroid a sol-ont:Asteroid ;
		sol-ont:hasCommonName ?name.
    ?asteroid sol-ont:hasAsteroidClassification ?type .
    ?type sol-ont:hasSMASSIIClass ?class.
    ?asteroid sol-ont:hasDistanceRecord ?record .
    ?record sol-ont:hasTemporalExtent ?te .
    ?te sol-ont:recordedAt ?time .
    ?record sol-ont:hasResult ?r. 
    ?r sol-ont:hasQuantity ?q.
    ?q sol-ont:hasQuantityValue ?qv .
    ?qv sol-ont:hasNumericValue ?distance .
    FILTER(
      (?time >= "2025-01"^^xsd:gYearMonth &&
      ?time < "2026-01"^^xsd:gYearMonth) &&
      ?distance < 1.5
    )
  } 
}
GROUP BY ?class
ORDERBY DESC (?CountOfTypes)
LIMIT 3
```
**Results:**
|AsteroidType|CountOfTypes|
|------------|------------|
|< http://soloflife.org/lod/resource/Cg >|4           |
|< http://soloflife.org/lod/resource/B >|3           |
|< http://soloflife.org/lod/resource/Xk >|1           |

## 3. Closest Asteroids In 2 Years Window
**Competency Question:** "Which is the closest asteroid to Earth in the next 24 months and when does that occur?"

**Bridged Datasets:** sbdb_jpl_asteroids_with_constraints.csv, Asteroid_Distances.csv 

**SPARQL Query:**
```sql
SELECT ?name ?time ?distance ?unit
WHERE {
  {
    SELECT *
    WHERE {
    ?asteroid a sol-ont:Asteroid .
    ?asteroid sol-ont:hasCommonName ?name .
    ?asteroid sol-ont:hasDistanceRecord ?record
    }
  } . 
  {
    SELECT *
    WHERE {
      ?record a sol-ont:DistanceRecord .
      ?record sol-ont:hasTemporalExtent ?te .
      ?te sol-ont:recordedAt ?time .
      ?record sol-ont:hasResult ?r .
      ?r sol-ont:hasQuantity ?q .
      ?q sol-ont:hasQuantityValue ?qv .
      ?qv a sol-ont:QuantityValue;
         sol-ont:hasNumericValue ?distance;
         sol-ont:hasUnit ?unit .
      FILTER( 
        ?time >= "2023-01"^^xsd:gYearMonth &&
        ?time <= "2025-05"^^xsd:gYearMonth
      )
    }
    ORDERBY ASC(?distance)
  }
}
```
**Results:**
| name    | time    | distance | unit |
|---------|---------|----------|------|
| Didymos | 2023-01 | 0.27677  | au   |
| Bennu   | 2024-05 | 0.42804  | au   |
| Ryugu   | 2025-05 | 0.44189  | au   |
| Bennu   | 2025-01 | 0.52983  | au   |
| Bennu   | 2023-08 | 0.5301   | au   |
| Bennu   | 2024-08 | 0.54087  | au   |
| Ryugu   | 2024-11 | 0.55874  | au   |
| Didymos | 2025-01 | 0.56544  | au   |
| Didymos | 2024-08 | 0.61461  | au   |
| Bennu   | 2025-05 | 0.64079  | au   |
| Didymos | 2024-11 | 0.64674  | au   |
| Ryugu   | 2025-01 | 0.66498  | au   |
| Bennu   | 2024-11 | 0.7039   | au   |
| Bennu   | 2023-11 | 0.71025  | au   |

## 4. Top 5 Closest Iron Asteroids
**Competency Question:** "What are the 5 closest asteroids that may contain iron?"

**Bridged Datasets:** sbdb_jpl_asteroids_with_constraints.csv, Asteroid_Distances.csv, Summary_of_Asteroid_Taxonomic_Classes.csv
```sql
SELECT Distinct ?name
WHERE {
  ?asteroid a sol-ont:Asteroid;
  	sol-ont:hasCommonName ?name;
    sol-ont:hasAsteroidClassification ?class;
  	sol-ont:hasDistanceRecord ?record.
  ?record sol-ont:hasResult ?r. 
  ?r sol-ont:hasQuantity ?q.
  ?q sol-ont:hasQuantityValue ?qv .
  ?qv sol-ont:hasNumericValue ?distance .
  ?class a sol-ont:AsteroidClassification;
    sol-ont:hasSMASSIIClass ?smassii.
  ?smassii sol-ont:hasElementalComposition ?ec.
  ?ec sol-ont:hasElement ?e.
  FILTER(?e = "iron"^^sol-ont:ChemicalElement)
}
ORDERBY ASC(?distance)
```

**Results:**
| name |  
| :----: | 
| Didymos |
| Ryugu |
| Bennu |

## 5. Top 3 Profitable Asteroids in 2024
**Competency Question:** "What are the 3 most potentially profitable asteroids within 0.75au of Earth in 2024?"

**Bridged Datasets:** Asteroid_Distances.csv, Asterank_Dataset.csv

```sql
SELECT distinct ?name 
WHERE{
  {
	?asteroid sol-ont:hasCommonName ?name ;
    	sol-ont:hasDistanceRecord ?record ;
    	sol-ont:hasObservation ?obs .
    ?obs sol-ont:generatedBy ?activity .
    ?obs sol-ont:hasResult ?result .
    ?result sol-ont:hasQuantity ?q .
    ?q sol-ont:hasQuantityValue ?qv .
    ?qv sol-ont:hasNumericValue ?profit .
    ?record sol-ont:hasResult ?recordResult .
    ?record sol-ont:hasTemporalExtent ?te .
    ?te sol-ont:recordedAt ?time .
  	?recordResult sol-ont:hasQuantity ?recQ .
    ?recQ sol-ont:hasQuantityValue ?recQV .
    ?recQV sol-ont:hasNumericValue ?distance .
  }  
FILTER(
    ?activity=<http://soloflife.org/lod/resource/ProfitMeasurementActivity> &&
    (?time >= "2024-01"^^xsd:gYearMonth &&
      ?time <= "2024-11"^^xsd:gYearMonth)&&
    ?distance < 0.75
)
}
ORDERBY DESC(?profit)
```
**Results:** 
|name   |
|-------|
|Ryugu  |
|Didymos|
|Bennu  |

## 6. Ryugu Arriving
**Competency Question:** "When will 162173 Ryugu will be within 1au of Earth?"

**Bridged Datasets:** sbdb_jpl_asteroids_with_constraints.csv, Asteroid_Distances.csv

**SPARQL Query:**
```sql
SELECT ?distance ?time
WHERE {
  {
    ?asteroid a sol-ont:Asteroid ;
  				sol-ont:hasCommonName "Ryugu".
    ?asteroid sol-ont:hasDistanceRecord ?record .
    ?record sol-ont:hasTemporalExtent ?te .
    ?te sol-ont:recordedAt ?time .
    ?record sol-ont:hasResult ?r. 
    ?r sol-ont:hasQuantity ?q.
    ?q sol-ont:hasQuantityValue ?qv .
    ?qv sol-ont:hasNumericValue ?distance .
    FILTER(
      ?distance < 1)
  }}
```

**Results:**
| distance | time    |
|----------|---------|
| 0.8274   | 2024-08 |
| 0.55874  | 2024-11 |
| 0.66498  | 2025-01 |
| 0.44189  | 2025-05 |
| 0.6127   | 2025-08 |
| 0.83492  | 2029-05 |
| 0.3926   | 2029-08 |
| 0.67229  | 2029-11 |
| 0.69894  | 2030-01 |
| 0.66023  | 2030-05 |

## 7. Ryugu Length of Stay
**Competency Question:** "How long will 162173 Ryugu be within 1au of Earth?"

**Bridged Datasets:** sbdb_jpl_asteroids_with_constraints.csv, Asteroid_Distances.csv

**SPARQL Query:**
```sql
SELECT ?timeStart ?timeEnd ?duration
WHERE {  
  {
    SELECT ?timeStart 
    WHERE{
        ?asteroid sol-ont:hasCommonName ?name ;
              sol-ont:hasDistanceRecord ?record .
        ?record sol-ont:hasTemporalExtent ?te .
        ?te sol-ont:recordedAt ?timeStart .
        ?record sol-ont:hasResult ?r .
        ?r sol-ont:hasQuantity ?q .
        ?q sol-ont:hasQuantityValue ?qv .
        ?qv a sol-ont:QuantityValue;
        sol-ont:hasNumericValue ?distance;
        sol-ont:hasUnit ?unit .      
        Filter(
            ?name="Ryugu"
            && ?distance < 1
        ) 
      }ORDERBY(?timeStart) LIMIT 1
  }
  .
  {
    SELECT ?timeEnd
    WHERE{
        ?asteroid sol-ont:hasCommonName ?name ;
                sol-ont:hasDistanceRecord ?record .
        ?record sol-ont:hasTemporalExtent ?te .
        ?te sol-ont:recordedAt ?timeEnd .
        ?record sol-ont:hasResult ?r .
        ?r sol-ont:hasQuantity ?q .
        ?q sol-ont:hasQuantityValue ?qv .
        ?qv a sol-ont:QuantityValue;
        sol-ont:hasNumericValue ?distance;
        sol-ont:hasUnit ?unit .      
        Filter(
            ?name="Ryugu"
            && ?distance > 1
        )
      } 
  }
  FILTER(?timeEnd>?timeStart)
  BIND((?timeEnd-?timeStart) as ?duration)
} LIMIT 1
```

**Results:**
| timeStart | timeEnd | duration         |
|-----------|---------|------------------|
| 2024-08   | 2025-11 | P457DT0H0M0.000S |

## 8. Ryugu Distance After Range
**Competency Question:** "Based on current trajectory of 162173 Ryugu, how far from Earth will 162173 Ryugu be in 8 months?"

**Bridged Datasets:** Asteroid_Distances.csv


**SPARQL Query:**
```sql
SELECT ?Asteroid ?distance ?Unit
WHERE {
      ?Asteroid a sol-ont:Asteroid .
      ?Asteroid sol-ont:hasCommonName "Ryugu" .   
      ?Asteroid sol-ont:hasDistanceRecord ?d .
      ?d sol-ont:hasTemporalExtent ?time .
      ?time sol-ont:recordedAt "2024-01"^^xsd:gYearMonth .
      ?d sol-ont:hasResult ?r .
      ?r sol-ont:hasQuantity ?q .
      ?q sol-ont:hasQuantityValue ?qv .
      ?qv sol-ont:hasNumericValue ?distance .  
  		?qv sol-ont:hasUnit ?Unit .
} 
```
**Results:**
| Asteroid | distance | Unit |
| :----: | :----: | :----: |
| Ryugu | 2.06539e0 | au |


## 9. Planning for Ryugu
**Competency Question:** "How much time is available until the 162173 Ryugu is within 1au of Earth?"

**Bridged Datasets:** Asteroid_Distances.csv

**SPARQL Query:**
```sql
SELECT ?timeEnter ?distance1 ?timeArrive ?distance2 ?TimeRemaining
WHERE {  
  {
    SELECT ?timeEnter ?distance1
    WHERE{
        ?asteroid sol-ont:hasCommonName ?name ;
              sol-ont:hasDistanceRecord ?record .
        ?record sol-ont:hasTemporalExtent ?te .
        ?te sol-ont:recordedAt ?timeEnter .
        ?record sol-ont:hasResult ?r .
        ?r sol-ont:hasQuantity ?q .
        ?q sol-ont:hasQuantityValue ?qv .
        ?qv a sol-ont:QuantityValue;
        sol-ont:hasNumericValue ?distance1;
        sol-ont:hasUnit ?unit .      
        Filter(
            ?name="Ryugu"
            && ?distance1 > 1
        ) 
      }ORDERBY(?timeEnter) LIMIT 1
  }
  .
  {
    SELECT ?timeArrive ?distance2
    WHERE{
        ?asteroid sol-ont:hasCommonName ?name ;
                sol-ont:hasDistanceRecord ?record .
        ?record sol-ont:hasTemporalExtent ?te .
        ?te sol-ont:recordedAt ?timeArrive .
        ?record sol-ont:hasResult ?r .
        ?r sol-ont:hasQuantity ?q .
        ?q sol-ont:hasQuantityValue ?qv .
        ?qv a sol-ont:QuantityValue;
        sol-ont:hasNumericValue ?distance2;
        sol-ont:hasUnit ?unit .      
        Filter(
            ?name="Ryugu"
            && ?distance2 < 1
        )
      } LIMIT 1
  }
  FILTER(?timeArrive>?timeEnter)
  BIND((?timeArrive-?timeEnter) as ?TimeRemaining)
}  
```
**Results:**
| timeEnter | distance1 | timeArrive | distance2 | timeRemaining     |
|-----------|-----------|------------|-----------|-------------------|
| 2023-01   | 2.38984e0 | 2024-08    | 0.8274e0  | P577DT23H0M0.000S |

## 10. Iron Arrival
**Competency Question:** "Which asteroid is the first to come within 0.5au of Earth that contains iron?"

**Bridged Datasets:** sbdb_jpl_asteroids_with_constraints.csv, Asteroid_Distances.csv, Summary_of_Asteroid_Taxonomic_Classes.csv

**SPARQL Query:**
```sql
SELECT ?name ?distance ?time
WHERE {
  ?asteroid a sol-ont:Asteroid;
  	sol-ont:hasCommonName ?name;
    sol-ont:hasAsteroidClassification ?class;
  	sol-ont:hasDistanceRecord ?record.
  ?record sol-ont:hasResult ?r. 
  ?record sol-ont:hasTemporalExtent ?te .
  ?te sol-ont:recordedAt ?time .
  ?r sol-ont:hasQuantity ?q.
  ?q sol-ont:hasQuantityValue ?qv .
  ?qv sol-ont:hasNumericValue ?distance .
  ?class a sol-ont:AsteroidClassification;
    sol-ont:hasSMASSIIClass ?smassii.
  ?smassii sol-ont:hasElementalComposition ?ec.
  ?ec sol-ont:hasElement ?e.
  FILTER(
    ?e = "iron"^^sol-ont:ChemicalElement
  &&?distance < 1
  )
}
ORDERBY ASC(?time)
```
**Results:**
| name    | distance | time    |
|---------|----------|---------|
| Didymos | 0.27677  | 2023-01 |
| Bennu   | 0.5301   | 2023-08 |
| Bennu   | 0.71025  | 2023-11 |
| Bennu   | 0.85044  | 2024-01 |
| Bennu   | 0.42804  | 2024-05 |
| Didymos | 0.61461  | 2024-08 |
| Ryugu   | 0.8274   | 2024-08 |
| Bennu   | 0.54087  | 2024-08 |
| Didymos | 0.64674  | 2024-11 |
| Ryugu   | 0.55874  | 2024-11 |
| Bennu   | 0.7039   | 2024-11 |
| Didymos | 0.56544  | 2025-01 |
| Ryugu   | 0.66498  | 2025-01 |
| Bennu   | 0.52983  | 2025-01 |
| Ryugu   | 0.44189  | 2025-05 |

### Remarks
- `Asterank_Dataset.csv`:  refers to the `JPL_SBDB` dataset with Asterank's evaluation on Asteroid value and profitability
- `Asteroid_Distances.csv`:  refers to a subset of available Asteroids from `SkyLive`
- `sbdb_jpl_asteroids_with_constraints.csv`: refers to large set of sbdb_jpl dataset 
- `Summary_of_Asteroid_Taxonomic_Classes.csv`:  refers to the [Asteroid Spectral Types](https://en.wikipedia.org/wiki/Asteroid_spectral_types)
- `mp3c_dataset.csv`:  refers to a subset of MP3c's dataset of Asteroids
- `nasajpl_sbdl.csv`:  refers to a subset of NASA's JPL_SBDB dataset of Asteroids
