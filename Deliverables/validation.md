# Validation

## Template Copy Me
**Competency Question:** "What am I?"

**Bridged Datasets:** dataset 1, dataset 2, ...

**SPARQL Query:**
```sql
SELECT * WHERE {
	?s ?p ?o .
}
```

**Results:**
| Header |
| :----: |
| Result |
| Result |
| Result |
| Result |
| Result |

## Top 3 Most Frequent Occurring Mineral
**Competency Question:** "What are the top 3 most frequently occuring minerals within 1.5 astronomical units from Earth on January 2024?"

**Bridged Datasets:** 

**SPARQL Query:**
```sql
Select (?e as ?Element) (count(?e) as ?CountOfElement)
Where{
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
      ?time="JAN24"^^time:MonthOfYear
   	&& ?distance < 1.5
    )
  } 
}
GROUP BY ?e
ORDERBY DESC (?CountOfElement)
```

**Results:**
| Element | CountOfElement |
| :----: | :----: |
| ammonia | 1 |
| hydrogen | 1 |
| iron | 1 |
| nitrogen | 1 |

## Top 5 Most Occurring Asteroid Types
**Competency Question:** "What are the top 5 most occuring asteroid types within 1.5au from Earth on January 2024?"

**Bridged Datasets:** SOL_Asteroid_Names*, Asterank.csv, Summary_of_Asteroid_Taxonomic_Classes.csv

**SPARQL Query:**
```sql
Select (?class as ?AsteroidType) (count(?class) as ?CountOfTypes)
Where{
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
      ?time="JAN24"^^time:MonthOfYear
   	&& ?distance < 1.5
    )
  } 
}
GROUP BY ?class
ORDERBY DESC (?CountOfTypes)
```
**Results:**
| AsteroidType | CountofTypes |
| :----: | :----: |
| B | 1 |

## Closest Asteroids In 2 Years Window
**Competency Question:** "Which is the closest asteroid to Earth in the next 24 months and when does that occur?"

**Bridged Datasets:** SOL_Asteroid_Names*, Asteroid_Distances.csv 

**SPARQL Query:**
```sql
Select ?name ?time ?distance ?unit
Where{
  {
    Select *
    Where {
    ?asteroid a sol-ont:Asteroid .
    ?asteroid sol-ont:hasCommonName ?name .
    ?asteroid sol-ont:hasDistanceRecord ?record
    }
  } . 
  {
    Select *
    Where {
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
        ?time = "JAN23"^^time:MonthOfYear ||
        ?time = "MAY23"^^time:MonthOfYear ||
        ?time = "AUG23"^^time:MonthOfYear ||
        ?time = "NOV23"^^time:MonthOfYear ||
        ?time = "JAN24"^^time:MonthOfYear ||
        ?time = "MAY24"^^time:MonthOfYear ||
        ?time = "AUG24"^^time:MonthOfYear ||
        ?time = "NOV24"^^time:MonthOfYear ||
        ?time = "JAN25"^^time:MonthOfYear ||
        ?time = "MAY25"^^time:MonthOfYear
      )
    }
    ORDERBY ASC(?distance)
  }
}
```
**Results:**
| name | time | distance | unit | 
| :----: | :----: | :----: | :----: |
| Didymos | JAN23 | 0.27677 | au |
| Bennu | MAY24 | 0.42804 | au |
| Ryugu | MAY25 | 0.44189 | au |
| Bennu | JAN25 | 0.52983 | au |
| Bennu | AUG23 | 0.5301 | au |
| Bennu | AUG24 | 0.54087 | au |
| Ryugu | NOV24 | 0.55874 | au |
| Didymos | JAN25 | 0.56544 | au |
| Didymos | AUG24 | 0.61461 | au |
| Bennu | MAY25 | 0.64079 | au |
| Didymos | NOV24 | 0.64674 | au |
| Ryugu | JAN25 | 0.66498 | au |
| Bennu | NOV24 | 0.7039 | au |
| Bennu | NOV23 | 0.71025 | au |
| Ryugu | AUG24 | 0.8274 | au |
| Bennu | JAN24 | 0.85044 | au |

## Top 5 Closest Iron Asteroids
**Competency Question:** "What are the 5 closest asteroids that may contain iron?"

**Bridged Datasets:** SOL_Asteroid_Names*, Asteroid_Distances.csv, Summary_of_Asteroid_Taxonomic_Classes.csv
```sql
Select Distinct ?name
Where{
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

## Top 3 Profitable Asteroids in 2024
**Competency Question:** "What are the 3 most potentially profitable asteroids within 0.75au of Earth on January 2024?"

**Bridged Datasets:** Asteroid_Distances.csv, Asterank_Dataset.csv

```sql
SELECT ?name ?distance ?time ?profit
WHERE {
  {
    ?asteroid a sol-ont:Asteroid ;
  				sol-ont:hasCommonName ?name.
    ?asteroid sol-ont:hasDistanceRecord ?record .
    ?record sol-ont:hasTemporalExtent ?te .
    ?te sol-ont:recordedAt ?time .
    ?record sol-ont:hasResult ?r. 
    ?r sol-ont:hasQuantity ?q.
    ?q sol-ont:hasQuantityValue ?qv .
    ?qv sol-ont:hasNumericValue ?distance .
    FILTER(
        (?time = "JAN24"^^time:MonthOfYear ||
        ?time = "MAY24"^^time:MonthOfYear ||
        ?time = "AUG24"^^time:MonthOfYear ||
        ?time = "NOV24"^^time:MonthOfYear) &&
      	?distance < .75)
  }
  union 
  {
    ?asteroid a sol-ont:Asteroid ;
  				sol-ont:hasCommonName ?name.
  	?asteroid sol-ont:hasObservation ?obs . 
    ?obs sol-ont:hasResult ?or .
    ?or sol-ont:hasQuantity ?oq .
    ?oq sol-ont:hasQuantityKind "Profit"^^sol-qk:Profit .
    ?oq sol-ont:hasQuantityValue ?oqv .
    ?oqv sol-ont:hasNumericValue ?profit .
  FILTER (
    (?asteroid=<http://soloflife.org/lod/resource/Asteroid.1999_JU3> && ?oq=<http://soloflife.org/lod/resource/ProfitMeasurementQuantity.1999_JU3>) ||
    (?asteroid=<http://soloflife.org/lod/resource/Asteroid.1999_RQ36> && ?oq=<http://soloflife.org/lod/resource/ProfitMeasurementQuantity.1999_RQ36>) ||
    (?asteroid=<http://soloflife.org/lod/resource/Asteroid.1996_GT> && ?oq=<http://soloflife.org/lod/resource/ProfitMeasurementQuantity.1996_GT>))
  }
  
} ORDERBY ASC(?profit)
```
**Results:** 
|name   |distance |time |profit  |
|-------|---------|-----|--------|
|Didymos|0.61461e0|AUG24|        |
|Didymos|0.64674e0|NOV24|        |
|Ryugu  |0.55874e0|NOV24|        |
|Bennu  |0.42804e0|MAY24|        |
|Bennu  |0.54087e0|AUG24|        |
|Bennu  |0.7039e0 |NOV24|        |
|Bennu  |         |     |1.85E8  |
|Didymos|         |     |1.641E10|
|Ryugu  |         |     |3.008E10|


## Ryugu Arriving
**Competency Question:** "When will 162173 Ryugu enter within 1au of Earth?"

**Bridged Datasets:** SOL_Asteroid_Names*, Asteroid_Distances.csv

**SPARQL Query:**
```sql

```

## Ryugu Length of Stay
**Competency Question:** "How long will 162173 Ryugu be within 1au of Earth?"

**Bridged Datasets:** SOL_Asteroid_Names*, Asteroid_Distances.csv

**SPARQL Query:**
```sql

```

## Ryugu Departing
**Competency Question:** "When will a 162173 Ryugu exit a 1au range from Earth?"

**Bridged Datasets:** SOL_Asteroid_Names*, Asteroid_Distances.csv

**SPARQL Query:**
```sql

```

## Ryugu Distance After Range
**Competency Question:** "Based on current trajectory of 162173 Ryugu, how far from Earth will 162173 Ryugu be in 8 months?"

**Bridged Datasets:** Asteroid_Distances.csv


**SPARQL Query:**
```sql
SELECT ?Asteroid ?NumericValue ?Unit
WHERE {
      ?Asteroid a sol-ont:Asteroid .
      ?Asteroid sol-ont:hasCommonName "Ryugu" .   
      ?Asteroid sol-ont:hasDistanceRecord ?d .
      ?d sol-ont:hasTemporalExtent ?time .
      ?time sol-ont:recordedAt "JAN24"^^time:MonthOfYear .
      ?d sol-ont:hasResult ?r .
      ?r sol-ont:hasQuantity ?q .
      ?q sol-ont:hasQuantityValue ?qv .
      ?qv sol-ont:hasNumericValue ?NumericValue .  
  		?qv sol-ont:hasUnit ?Unit .
} 
LIMIT 10
```
**Results:**
| Asteroid | NumericValue | Unit |
| :----: | :----: | :----: |
| <http://soloflife.org/lod/resource/Asteroid.1999_JU3> | "2.06539e0"^^<http://www.w3.org/2001/XMLSchema#double> | "au"^^<http://soloflife.org/lod/unitsau> |


## Planning for Ryugu
**Competency Question:** "How much time is available until the 162173 Ryugu is within 1au of Earth?"

**Bridged Datasets:** Asteroid_Distances.csv

## Iron Arrival
**Competency Question:** "Which asteroid is the first to come within 0.5au of Earth that contains iron?"

**Bridged Datasets:** SOL_Asteroid_Names*, Asteroid_Distances.csv, Summary_of_Asteroid_Taxonomic_Classes.csv

**SPARQL Query:**
```sql
Select ?name ?distance ?time
Where{
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
| name    | distance | time  |
|---------|----------|-------|
| Bennu   | 0.5301   | AUG23 |
| Didymos | 0.61461  | AUG24 |
| Ryugu   | 0.8274   | AUG24 |
| Bennu   | 0.54087  | AUG24 |
| Ryugu   | 0.6127   | AUG25 |
| Ryugu   | 0.3926   | AUG29 |
| Bennu   | 0.66601  | AUG29 |
| Bennu   | 0.43106  | AUG30 |
| Didymos | 0.27677  | JAN23 |
| Bennu   | 0.85044  | JAN24 |
| Didymos | 0.56544  | JAN25 |
| Ryugu   | 0.66498  | JAN25 |
| Bennu   | 0.52983  | JAN25 |
| Ryugu   | 0.69894  | JAN30 |

### Remarks
- `Asterank_Dataset.csv`:  refers to the `JPL_SBDB` dataset with Asterank's evaluation on Asteroid value and profitability
- `Asteroid_Distances.csv`:  refers to a subset of available Asteroids from `SkyLive`
- `Summary_of_Asteroid_Taxonomic_Classes.csv`:  refers to the [Asteroid Spectral Types](https://en.wikipedia.org/wiki/Asteroid_spectral_types)
- `mp3c_dataset.csv`:  refers to a subset of MP3c's dataset of Asteroids
- `nasajpl_sbdl.csv`:  refers to a subset of NASA's JPL_SBDB dataset of Asteroids
