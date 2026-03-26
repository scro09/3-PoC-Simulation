# 3-PoC-Simulation
3 PoC Simulation

## Executive Summary
The goal of this Proof of Concept (POC) was to take a raw, messy dataset of supplier inputs from a client and accurately map them to verified, real-world company entities. 

## Step 1 — Deduplication
**The thought process:**  
Before applying any complex matching logic, I first analyzed the structure of the dataset. In real-world procurement data, duplicates are common, so the first step was to identify and remove them.

I used exact matching on key fields to eliminate duplicate records.

Depending on the combination of fields used, different deduplication results were obtained. In the final version, I used almost all relevant fields and observed that there were no significant duplicates, meaning the dataset was clean and ready for the next step.

### Output:
- `no_dup_rows.csv`

## Step 2 — Entity Matching

A rule-based scoring system selects the **best match per company**.

### Scoring Logic

 Feature | Score 
 Name word overlap  50 
 Country match  +25 
 Region match  +15 
 City match +10
 
### Process:
- Normalize text (lowercase, trim spaces)
- Split company names into word sets
- Compute overlap score
- Add location-based bonuses
- Select highest scoring match per group

### Threshold:
A similarity threshold is used to decide whether a candidate match is valid or not.
threshold = 50

### Output:
- `best_matches.csv`
-  `unmatched_rows.csv`

## Step 3 - Solving unmatched cases

Take unmatched cases and find the correct entity on the web using **DuckDuckGo Search (ddgs)**.
Then we extract the **top search result (title + URL)** to enrich missing entities.

### Output:
- `solvedunmathched.csv`

## Why my implemenattion is good 
- Combines **structured matching + real-world web validation**
- Uses a **simple and fast rule-based scoring system**
- Is **fully interpretable and easy to debug**
- Improves coverage by handling **unmatched cases via web search**
- Keeps the pipeline **modular and scalable**
- Adds **external knowledge source (DDGS)** for better accuracy

 ## Weak Points / Limitation
 
 Web search latency (Step 3)
- The **unmatched enrichment step is slow** because each record triggers an external web search
- Performance depends on network speed and DDGS response time
- Not suitable for real-time or large-scale batch processing without optimization

  ### Multiple intermediate files
- The pipeline generates multiple output files at each step:
  - `no_dup_rows.csv`
  - `best_matches.csv`
  - `unmatched_rows.csv`
  - `solved_unmatched.csv`
    
The use of multiple intermediate files was intentional for clarity and learning purposes, as it makes each stage of the pipeline easy to understand, debug, and validate independently.
