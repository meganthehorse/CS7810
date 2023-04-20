# Brandon Critique
**Author:** Brandon Dave

## Group 3: Group 3
**Members:** Antrea Christou, Erin Rogers, Sydney Woods
### Summary
The group's ontology focuses on querying information about aircraft vehicles (various planes) and manufacturers of the necessary parts of the vehicles.

### Strengths
- The group is able to confidently defend their axioms even if the schema did not match up in the final stages.
- The details the group provided allowed me to follow along with the presentation and motivations without needing to be concerned about not fully understanding the research topic itself.
- I enjoyed that Erin through detailing of varying Crash Types that could be implemented into the ontology and why Crash Types was an important entity rather than a String description.
- Detailing of FAA Documentation causing issues showcasing a before-and-after of the schema diagram
  - The group described what the schema *could* be if the documentation/data was digitized
- Effective use of detailing inverse relationships without being excessive

### Weaknesses
- The group created some schemas that could have followed a pattern from MODL - one of their entries appeared to be a MODL Record.
    - However, the group defended their actions of not using patterns
- The group described their axioms with "isA" relationships which would imply Super-Sub Class relationship; however, the schema itself used an arrow defining a relationship to the objects.

### Additional Notes:
- Is there a standard to plane identification numbers? Could the ontology be improved to include the standard as [NC]+[#####], the provided example from Erin.

## Driving Project Ontology
**Members:** Alexander Moore, CJ Menart, Jehan Fernando
### Summary
The group was interested in utilizing ontology to apply knowledge on surrounding objects that would support self-driving vehicles and the "acionable plans" the vehicle takes.

### Strengths
- The group had an effective display of the pitfalls they encountered during materialization and how they worked around them
- Well-thought out Scenario types and how to incorporate Weather Conditions to Driving Conditions
- The group discusses their omission of car details as it did not affect the overall goal of the ontology
- I enjoyed how the last slide, featuring the Scenario as an Image with the Results of the SPARQL query, tied the group's efforts to a conclusory note.

### Weaknesses
- The naming conventions of some of the ontology entities are confusing; such as, querying on "On-Left-Right.On".
- It took me a while to realize what a "Scenario" was in the ontology.  I later discovered it was just a snapshot situation of what the vehicle perceives at a given moment.
- I was not sure what I was viewing during the "Extra Annotations" slide.  Were these results the group formulated or were they additional notes from CityScapes dataset?
- The schema diagram was scaled-up when objects could have been modeled towards a tighter layout. DataType diagramming did not follow any firm color standard and the shape heights were slightly distracting.
    - Although not breaking point, the Scenario and Potential Obstacle Arrows were irregular to the other schemas which had some uniformity through angles.

### Additional Notes:
- For future research, it would be interesting to utilize an image classification model on CityScape Scenario images and seeing if the ontology could still come to conclusions if a car is allowed to produce a maneuver!