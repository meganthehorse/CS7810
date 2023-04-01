# Validation

## Template Copy Me
**Competency Question:** "What am I?"

**Bridged Datasets:** dataset 1, dataset 2, ...

**SPARQL Query:**
```
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

## Top 3 Most Frequent Occurring Minderal
**Competency Question:** "What are the top 3 most frequently occuring minerals within 1.5 astronomical units from Earth on January 2024?"

**Bridged Datasets:** dataset 1, dataset 2, ...

**SPARQL Query:**
```
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

## Top 5 Most Occurring Asteroid Types
**Competency Question:** "What are the top 5 most occuring asteroid types within 1.5au from Earth on January 2024?"

**Bridged Datasets:** dataset 1, dataset 2, ...

**SPARQL Query:**
```
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

## Closest Asteroids In 2 Years Window
**Competency Question:** "Which is the closest asteroid to Earth in the next 24 months and when does that occur?"

**Bridged Datasets:** Asteroid_Distances.csv 

## Top 5 Closest Iron Asteroids
**Competency Question:** "What are the 5 closest asteroids that may contain iron?"

**Bridged Datasets:** Asteroid_Distances.csv, Summary_of_Asteroid_Taxonomic_Classes.csv

## Top 3 Profitable Asteroids in 2024
**Competency Question:** "What are the 3 most potentially profitable asteroids within 0.75au of Earth on January 2024?"

**Bridged Datasets:** Asteroid_Distances.csv, Asterank_Dataset.csv

## Ryugu Arriving
**Competency Question:** "When will 162173 Ryugu enter within 1au of Earth?"

**Bridged Datasets:** Asteroid_Distances.csv

## Ryugu Length of Stay
**Competency Question:** "How long will 162173 Ryugu be within 1au of Earth?"

**Bridged Datasets:** Asteroid_Distances.csv

## Ryugu Departing
**Competency Question:** "When will a 162173 Ryugu exit a 1au range from Earth?"

**Bridged Datasets:** Asteroid_Distances.csv

## Ryugu Distance After Range
**Competency Question:** "Based on current trajectory of 162173 Ryugu, how far from Earth will 162173 Ryugu be in 8 months?"

**Bridged Datasets:** Asteroid_Distances.csv

## Planning for Ryugu
**Competency Question:** "How much time is available until the 162173 Ryugu is within 1au of Earth?"

**Bridged Datasets:** Asteroid_Distances.csv

## Iron Arrival
**Competency Question:** "Which asteroid is the first to come within 0.5au of Earth that contains iron?"

**Bridged Datasets:** Asteroid_Distances.csv, Summary_of_Asteroid_Taxonomic_Classes.csv

### Remarks
`Asterank_Dataset.csv`:  refers to the `JPL_SBDB` dataset with Asterank's evaluation on Asteroid value and profitability
`Asteroid_Distances.csv`:  refers to a subset of available Asteroids from `SkyLive`
`Summary_of_Asteroid_Taxonomic_Classes.csv`:  refers to the [Asteroid Spectral Types](https://en.wikipedia.org/wiki/Asteroid_spectral_types)
`mp3c_dataset.csv`:  refers to a subset of MP3c's dataset of Asteroids
`nasajpl_sbdl.csv`:  refers to a subset of NASA's JPL_SBDB dataset of Asteroids
