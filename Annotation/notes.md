# Notes on annotation data

## Interesting sentences:

- What I am really trying to get at is why should anyone in the public have to do such calculations?
- My understanding is that these rental units will be available for low to moderate income seniors.
- My understanding is that the Government will own 33 units and Oncore Seniors Society, received financing from the Government over a long period of time, and they will own the other 33 units. 
- Remember, the City does not collect any income tax. 
- We were at the point of knowing we would need to move, but didn’t want to move into any of the existing facilities in Prince George.
- He says it wasn’t until Mayor Lyn Hall was elected that the wheels were set in motion.

## Notes during annotation

- Some predicates are saved with u for unknown others will be with UNKN
- first instance of 'u' in the predicate is for an incorrectly labeled embedded clause that was actually a cleft.

## Fourth Pass

- Need to filter the database better

TODO:
- Add filtering heuristics to include:
    - Verb before SBAR
    - Some of the dependency parser markers
- Make the 1000 samples searched more random over the common crawl dataset


## Third pass

- Made the sentence presentation a little nicer
- Allowed for continuous progress

## Second Pass

- Annotation tool with keyboard input successful

## First Pass

- Filtered based on SBAR presence (<500/10000)

- Opening the data on excel to annotate has proven difficult.
    - Issues with character import
    - Will try to edit the pandas dataFrame directly to save in that format later

